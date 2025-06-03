#include "mapping.hpp"
#include <iomanip>  

void get_triface(
    const compas::RowMatrixXi& F_,
    int faceID, 
    const compas::RowMatrixXd& V, 
    compas::RowMatrixXd& A, 
    compas::RowMatrixXd& B, 
    compas::RowMatrixXd& C)
{
    if(0 <= faceID && faceID < F_.rows())
    {
        A = compas::RowMatrixXd(1, 3);
        B = compas::RowMatrixXd(1, 3);
        C = compas::RowMatrixXd(1, 3);
        if(V.cols() == 2)
        {
            A << V(F_(faceID, 0), 0), V(F_(faceID, 0), 1), 0;
            B << V(F_(faceID, 1), 0), V(F_(faceID, 1), 1), 0;
            C << V(F_(faceID, 2), 0), V(F_(faceID, 2), 1), 0;
        }
        else if(V.cols() == 3){
            A << V(F_(faceID, 0), 0), V(F_(faceID, 0), 1), V(F_(faceID, 0), 2);
            B << V(F_(faceID, 1), 0), V(F_(faceID, 1), 1), V(F_(faceID, 1), 2);
            C << V(F_(faceID, 2), 0), V(F_(faceID, 2), 1), V(F_(faceID, 2), 2);
        }
    }

    return;
}

bool map_point3d_simple(
    const compas::RowMatrixXi& F_, 
    const compas::RowMatrixXd& UV_, 
    const Eigen::Vector3d& pt, 
    Eigen::Vector3d& l, 
    int& faceID)
{
    if(UV_.isZero())
    {
        return false;
    }
    else{
        compas::RowMatrixXd P(1, 3), L(1, 3);
        P << pt(0), pt(1), pt(2);
        for(int id = 0; id < F_.rows(); id++)
        {
            compas::RowMatrixXd A, B, C;
            get_triface(F_, id, UV_, A, B, C);
            igl::barycentric_coordinates(P, A, B, C, L);
            if(L.minCoeff() < -1e-5 || L.maxCoeff() > 1 + 1e-5){
                continue;
            }
            else{
                l = Eigen::Vector3d(L(0, 0), L(0, 1), L(0, 2));
                faceID = id;
                return true;
            }
        }
    }

    return false;
}

std::vector<std::vector<int>> map_mesh(
    Eigen::Ref<const compas::RowMatrixXd> v, 
    Eigen::Ref<const compas::RowMatrixXi> f, 
    Eigen::Ref<const compas::RowMatrixXd> uv,
    
    Eigen::Ref<compas::RowMatrixXd> pattern_v, 
    const std::vector<std::vector<int>>& pattern_f, 
    Eigen::Ref<const compas::RowMatrixXd> pattern_uv)
{

    // Use regular MatrixXd to avoid type conflicts with AABB functions
    Eigen::MatrixXd V_uv = uv;
    Eigen::MatrixXi F_faces = f;
    
    igl::AABB<Eigen::MatrixXd, 2> tree;
    tree.init(V_uv, F_faces);

    std::vector<bool> inMesh;
    Eigen::MatrixXd C;
    Eigen::VectorXi I;
    Eigen::VectorXd sqrD;
    Eigen::MatrixXd pattern_uv_eigen = pattern_uv;
    
    tree.squared_distance(V_uv, F_faces, pattern_uv_eigen, sqrD, I, C);
    
    for(int id = 0; id < pattern_uv.rows(); id++)
    {
        if(std::fabs(sqrD[id]) < 1e-5) // Tolerance
        {
            compas::RowMatrixXd A, B, C;
            Eigen::MatrixXd P(1, 3);
            P << pattern_uv(id, 0), pattern_uv(id, 1), 0;
            compas::RowMatrixXd UV_A, UV_B, UV_C;
            get_triface(f, I(id), uv, UV_A, UV_B, UV_C);
            Eigen::MatrixXd L;
            igl::barycentric_coordinates(P, UV_A, UV_B, UV_C, L);

            inMesh.push_back(true);
            
            // Get 3D points for interpolation
            get_triface(f, I(id), v, A, B, C);
            // Update pattern vertex position through barycentric interpolation
            pattern_v.row(id) = A.row(0) * L(0, 0) + B.row(0) * L(0, 1) + C.row(0) * L(0, 2);
        }
        else{
            inMesh.push_back(false);
        }
    }

    // Filter out faces with vertices outside the target mesh

    // Convert pattern faces to std::vector<std::vector<int>> format for processing
    std::vector<std::vector<int>> pattern_polygonal_faces;
    for (int i = 0; i < pattern_f.size(); i++) {
        std::vector<int> face;
        // Handle any number of vertices per face, assuming -1 indicates end of face in some formats
        for (int j = 0; j < pattern_f[i].size(); j++) {
            int vertex_idx = pattern_f[i][j];
            // Some formats use -1 to mark end of face
            if (vertex_idx == -1) break;
            face.push_back(vertex_idx);
        }
        
        // Only add faces with at least 3 vertices
        if (face.size() >= 3) {
            pattern_polygonal_faces.push_back(face);
        }
    }

    for(std::vector<std::vector<int>>::iterator it = pattern_polygonal_faces.begin(); it != pattern_polygonal_faces.end();)
    {
        bool all_in_refMesh = true;
        // iterate vertices
        for(int jd = 0; jd < (*it).size(); jd++)
        {
            int vid = (*it)[jd];
            if(inMesh[vid] == false){
                all_in_refMesh = false;
                break;
            }
        }
        // After checking all vertices of the face, if all_in_refMesh is false (meaning at least one vertex is outside):
        if(!all_in_refMesh){
            it = pattern_polygonal_faces.erase(it);
        }
        else{
            it++;
        }
    }


    return pattern_polygonal_faces;
}

std::vector<std::vector<int>> map_mesh_cropped(
    Eigen::Ref<const compas::RowMatrixXd> v, 
    Eigen::Ref<const compas::RowMatrixXi> f, 
    Eigen::Ref<const compas::RowMatrixXd> uv,
    Eigen::Ref<compas::RowMatrixXd> pattern_v, 
    const std::vector<std::vector<int>>& pattern_f, 
    Eigen::Ref<const compas::RowMatrixXd> pattern_uv)
{

    // Use regular MatrixXd to avoid type conflicts with AABB functions
    Eigen::MatrixXd V_uv = uv;
    Eigen::MatrixXi F_faces = f;
    
    igl::AABB<Eigen::MatrixXd, 2> tree;
    tree.init(V_uv, F_faces);

    Eigen::MatrixXd C;
    Eigen::VectorXi I;
    Eigen::VectorXd sqrD;
    Eigen::MatrixXd pattern_uv_eigen = pattern_uv;
    
    // Find closest points on the mesh for all pattern vertices
    tree.squared_distance(V_uv, F_faces, pattern_uv_eigen, sqrD, I, C);
    
    // Map each pattern vertex to 3D using barycentric coordinates
    for(int id = 0; id < pattern_uv.rows(); id++)
    {
        Eigen::MatrixXd P(1, 3);
        P << pattern_uv(id, 0), pattern_uv(id, 1), 0;
        
        // Get UV coordinates of the target face
        compas::RowMatrixXd UV_A, UV_B, UV_C;
        get_triface(f, I(id), uv, UV_A, UV_B, UV_C);
        
        // Calculate barycentric coordinates
        Eigen::MatrixXd L;
        igl::barycentric_coordinates(P, UV_A, UV_B, UV_C, L);
        
        // Get 3D points of the target face
        compas::RowMatrixXd A, B, C;
        get_triface(f, I(id), v, A, B, C);
        
        // Update pattern vertex position through barycentric interpolation
        pattern_v.row(id) = A.row(0) * L(0, 0) + B.row(0) * L(0, 1) + C.row(0) * L(0, 2);

    }
    
    return pattern_f;
}

void rescale(Eigen::MatrixXd &V_uv)
{
    // Find min and max values for normalization
    Eigen::Vector2d min_coeff = V_uv.colwise().minCoeff();
    Eigen::Vector2d max_coeff = V_uv.colwise().maxCoeff();
    
    // Compute the size of the bounding box
    Eigen::Vector2d size = max_coeff - min_coeff;
    
    // Translate UV coordinates so minimum is at the origin
    V_uv.col(0) = V_uv.col(0).array() - min_coeff(0);
    V_uv.col(1) = V_uv.col(1).array() - min_coeff(1);
    
    // Scale to fit in a 0-1 box while maintaining aspect ratio
    double scale_factor = 1.0 / std::max(size(0), size(1));
    V_uv *= scale_factor;
}

// Check if any segment of path1 intersects with any segment of path2
bool PathIntersect(const Clipper2Lib::PathD& path1, const Clipper2Lib::PathD& path2, double scale) {
    // Check each segment of path1 against each segment of path2
    for (size_t i = 0; i < path1.size(); i++) {
        const Clipper2Lib::PointD& p1a = path1[i];
        const Clipper2Lib::PointD& p1b = path1[(i + 1) % path1.size()];
        
        for (size_t j = 0; j < path2.size(); j++) {
            const Clipper2Lib::PointD& p2a = path2[j];
            const Clipper2Lib::PointD& p2b = path2[(j + 1) % path2.size()];
            
            // Convert to Point64 for using with SegmentsIntersect
            Clipper2Lib::Point64 p1a64(static_cast<int64_t>(p1a.x * scale), static_cast<int64_t>(p1a.y * scale));
            Clipper2Lib::Point64 p1b64(static_cast<int64_t>(p1b.x * scale), static_cast<int64_t>(p1b.y * scale));
            Clipper2Lib::Point64 p2a64(static_cast<int64_t>(p2a.x * scale), static_cast<int64_t>(p2a.y * scale));
            Clipper2Lib::Point64 p2b64(static_cast<int64_t>(p2b.x * scale), static_cast<int64_t>(p2b.y * scale));
            
            if (Clipper2Lib::SegmentsIntersect(p1a64, p1b64, p2a64, p2b64))
                return true;  // Found an intersection
        }
    }
    
    return false;  // No intersections found
}


// For checking PathsD (collection of paths)
bool PathsIntersect(const Clipper2Lib::PathsD& paths1, const Clipper2Lib::PathsD& paths2, double scale) {
    // Check all combinations of paths
    for (const auto& path1 : paths1) {
        for (const auto& path2 : paths2) {
            if (PathIntersect(path1, path2, scale))
                return true;
        }
    }
    return false;
}


std::tuple<compas::RowMatrixXd, std::vector<std::vector<int>>> eigen_to_clipper (
    Eigen::Ref<const compas::RowMatrixXd> flattned_target_uv,
    Eigen::Ref<const compas::RowMatrixXi> target_f, 
    
    Eigen::Ref<const compas::RowMatrixXd> pattern_v, 
    const std::vector<std::vector<int>>& pattern_f
)   
{
 
    ////////////////////////////////////////////////////////////////////////////////////////
    // Get Boundary polygon of a Mesh as Clipper Path.
    ////////////////////////////////////////////////////////////////////////////////////////

    std::vector<std::vector<int>> L;
    igl::boundary_loop(target_f, L);
    Clipper2Lib::PathsD boundary;

    for (const auto &polyline_ids : L)
    {
        Clipper2Lib::PathD path;
        for (const auto &point_id : polyline_ids)
            path.emplace_back(flattned_target_uv(point_id, 0), flattned_target_uv(point_id, 1));
        
        boundary.push_back(path);
    }

    // Get the bounds of the boundary path
    Clipper2Lib::RectD boundary_bounds = Clipper2Lib::GetBounds(boundary);


    ////////////////////////////////////////////////////////////////////////////////////////
    // Check if pattern polygons are inside the boundary
    ////////////////////////////////////////////////////////////////////////////////////////
    

    // Convert the pattern polygons to clipper polygons.
    std::vector<Clipper2Lib::PathsD> patterns_to_cut;
    std::vector<Clipper2Lib::PathsD> patterns_to_keep;

    for (const auto &polyline_ids : pattern_f)
    {

        // Convert to clipper paths
        Clipper2Lib::PathsD paths;
        Clipper2Lib::PathD path;
        for (const auto &point_id : polyline_ids)
            path.emplace_back(pattern_v(point_id, 0), pattern_v(point_id, 1));
        paths.emplace_back(path);

        // Get bounds of current pattern polygon
        Clipper2Lib::RectD pattern_bounds = Clipper2Lib::GetBounds(paths);
        
        // Check if the pattern bounds intersect with boundary bounds
        if (!pattern_bounds.Intersects(boundary_bounds))
            continue;

        // Check if Elements are inside the boundary
        Clipper2Lib::PointD corners[] = {
            {pattern_bounds.left, pattern_bounds.top},      // Top-left
            {pattern_bounds.right, pattern_bounds.top},     // Top-right
            {pattern_bounds.right, pattern_bounds.bottom},  // Bottom-right
            {pattern_bounds.left, pattern_bounds.bottom}    // Bottom-left
        };

        bool is_rect_inside_polygon = false;
        size_t num_corners_in_polygon = 0;
        for (const auto& corner : corners) {
            auto result = Clipper2Lib::PointInPolygon(corner, boundary[0]);

            if (result != Clipper2Lib::PointInPolygonResult::IsOutside) {
                is_rect_inside_polygon = true;
                bool has_collision = PathsIntersect(paths, boundary);


                
                // check if the point is not in a hole
                bool is_rect_outside_polygon_hole = true;
                for (size_t i = 1; i < boundary.size(); i++) {                    
                    auto result = Clipper2Lib::PointInPolygon(corner, boundary[i]);
                    if (result != Clipper2Lib::PointInPolygonResult::IsOutside) {
                        is_rect_outside_polygon_hole = false;
                        break;
                    }
                }

                if (!has_collision && is_rect_inside_polygon && is_rect_outside_polygon_hole)
                    num_corners_in_polygon++;
            }
        }

        // Fully enclosed polygons are added to the keep list
        // Other polygons edges are intersected with the boundary
        if (num_corners_in_polygon == 4){
            patterns_to_keep.push_back(paths);
        } 
        else if (PathsIntersect(paths, boundary)){
            patterns_to_cut.push_back(paths);
        }


    }

    // perform intersection
    std::vector<Clipper2Lib::PathsD> solutions;
    for (const auto &subject : patterns_to_cut){
        Clipper2Lib::PathsD solution = Clipper2Lib::Intersect(subject, boundary, Clipper2Lib::FillRule::NonZero, 8);
        if (solution.size() == 0)
            continue;
        
        solutions.push_back(solution);
    }
    //solutions = patterns_to_cut;

    // Count total points
    size_t total_points = 0;
    for (const auto &solution : solutions) 
        for (const auto &path : solution) 
            total_points += path.size();

    for (const auto &subject : patterns_to_keep) 
        for (const auto &path : subject) 
            total_points += path.size();


    // We'll count the total points and then initialize our output matrices
    // These will be populated later
    std::vector<std::vector<int>> faces;
    faces.reserve(total_points); // This is an overestimation, but ensures capacity
    
    size_t point_index = 0; // Reset point index

    compas::RowMatrixXd vertices(total_points, 3);

    for (const auto &solution : solutions){
        for (const auto& path : solution) {
            std::vector<int> face;
            for (const auto& point : path) {
                vertices(point_index, 0) = point.x;
                vertices(point_index, 1) = point.y;
                vertices(point_index, 2) = 0;
                face.push_back(point_index);
                point_index++;
            }
            faces.push_back(face);
        }
    }

    for (const auto &subject : patterns_to_keep){
        for (const auto& path : subject) {
            std::vector<int> face;
            for (const auto& point : path) {
                vertices(point_index, 0) = point.x;
                vertices(point_index, 1) = point.y;
                vertices(point_index, 2) = 0; // Set z-coordinate to 0
                face.push_back(point_index);
                point_index++;
            }
            faces.push_back(face);
        }
    }

    // vertices = pattern_v;
    // faces = pattern_f;

    return std::make_tuple(vertices, faces);

}

std::tuple<compas::RowMatrixXd, std::vector<std::vector<int>>> map_mesh_with_automatic_parameterization(
    Eigen::Ref<const compas::RowMatrixXd> target_v, 
    Eigen::Ref<const compas::RowMatrixXi> target_f, 
    Eigen::Ref<compas::RowMatrixXd> pattern_v, 
    const std::vector<std::vector<int>>& pattern_f,
    bool clip_boundaries)
{


    // Compute target mesh UV parameterization using LSCM
    Eigen::MatrixXd target_uv;
    
    // Find the open boundary
    Eigen::VectorXi B;
    igl::boundary_loop(target_f, B);

    // Fix two points on the boundary
    Eigen::VectorXi fixed(2, 1);
    fixed(0) = B(0);
    fixed(1) = B(B.size() / 2);

    Eigen::MatrixXd fixed_uv(2, 2);
    fixed_uv << 0, 0, 1, 0;

    // LSCM parametrization
    igl::lscm(target_v, target_f, fixed, fixed_uv, target_uv);
    rescale(target_uv);


    // Choose whether to use clipped pattern or original pattern
    // For debugging, we're using the original pattern vertices and faces
    if (clip_boundaries) { // Set to false to use clipped pattern

        // Clip the pattern
        auto [clipped_pattern_v, clipped_pattern_f] = eigen_to_clipper(target_uv, target_f, pattern_v, pattern_f);

        //return std::make_tuple(clipped_pattern_v, clipped_pattern_f);

        Eigen::MatrixXd clipped_pattern_uv;
        clipped_pattern_uv.setZero();
        clipped_pattern_uv = clipped_pattern_v.leftCols(2);

        auto result = map_mesh_cropped(
            target_v, 
            target_f,
            target_uv,
            clipped_pattern_v,
            clipped_pattern_f,
            clipped_pattern_uv);


        return std::make_tuple(clipped_pattern_v, result);


    } else {

        Eigen::MatrixXd pattern_uv;
        pattern_uv.setZero();
        pattern_uv = pattern_v.leftCols(2);

        compas::RowMatrixXd pattern_v_copy = pattern_v;

        auto result = map_mesh(
            target_v, 
            target_f,
            target_uv,
            pattern_v_copy,
            pattern_f,
            pattern_uv);


        return std::make_tuple(pattern_v_copy, result);

    }
}


NB_MODULE(_mapping, m)
{
        
    m.def(
        "map_mesh_with_automatic_parameterization",
        &map_mesh_with_automatic_parameterization,
        "Map a 2D pattern mesh onto a 3D target mesh with automatic parameterization.",
        "target_v"_a,
        "target_f"_a,
        "target_uv"_a,
        "target_fixed_vid"_a,
        "clip_boundaries"_a = true);
}