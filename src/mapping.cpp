#include "mapping.hpp"

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
        // Prepare point for barycentric coordinate calculation
        Eigen::MatrixXd P(1, 3);
        P << pattern_uv(id, 0), pattern_uv(id, 1), 0;
        
        // Inline get_triface for UV coordinates
        int faceID = I(id);
        Eigen::MatrixXd UV_A(1, 3), UV_B(1, 3), UV_C(1, 3);
        
        if(0 <= faceID && faceID < f.rows()) {
            // UV coordinates
            UV_A << uv(f(faceID, 0), 0), uv(f(faceID, 0), 1), 0;
            UV_B << uv(f(faceID, 1), 0), uv(f(faceID, 1), 1), 0;
            UV_C << uv(f(faceID, 2), 0), uv(f(faceID, 2), 1), 0;
        }
        
        // Calculate barycentric coordinates
        Eigen::MatrixXd L;
        igl::barycentric_coordinates(P, UV_A, UV_B, UV_C, L);
        
        // Inline get_triface for 3D vertex positions
        Eigen::MatrixXd A(1, 3), B(1, 3), C(1, 3);
        
        if(0 <= faceID && faceID < f.rows()) {
            // 3D coordinates
            A << v(f(faceID, 0), 0), v(f(faceID, 0), 1), v(f(faceID, 0), 2);
            B << v(f(faceID, 1), 0), v(f(faceID, 1), 1), v(f(faceID, 1), 2);
            C << v(f(faceID, 2), 0), v(f(faceID, 2), 1), v(f(faceID, 2), 2);
        }
        
        // Update pattern vertex position through barycentric interpolation
        pattern_v.row(id) = A * L(0, 0) + B * L(0, 1) + C * L(0, 2);
    }
    
    
    return pattern_f;
}

// Check if any segment of path1 intersects with any segment of path2
bool path_intersect(const Clipper2Lib::PathD& path1, const Clipper2Lib::PathD& path2, double scale) {
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
bool paths_intersect(const Clipper2Lib::PathsD& paths1, const Clipper2Lib::PathsD& paths2, double scale) {
    // Check all combinations of paths
    for (const auto& path1 : paths1) {
        for (const auto& path2 : paths2) {
            if (path_intersect(path1, path2, scale))
                return true;
        }
    }
    return false;
}


std::tuple<compas::RowMatrixXd, std::vector<std::vector<int>>> eigen_to_clipper (
    Eigen::Ref<const compas::RowMatrixXd> flattned_target_uv,
    Eigen::Ref<const compas::RowMatrixXi> target_f, 
    
    Eigen::Ref<const compas::RowMatrixXd> pattern_v, 
    const std::vector<std::vector<int>>& pattern_f,
    bool clip_boundaries
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
        // Clipper2Lib::PointD corners[] = {
        //     {pattern_bounds.left, pattern_bounds.top},      // Top-left
        //     {pattern_bounds.right, pattern_bounds.top},     // Top-right
        //     {pattern_bounds.right, pattern_bounds.bottom},  // Bottom-right
        //     {pattern_bounds.left, pattern_bounds.bottom}    // Bottom-left
        // };

        bool is_rect_inside_polygon = false;
        size_t num_corners_in_polygon = 0;
        for (const auto& corner : paths[0]) {
            auto result = Clipper2Lib::PointInPolygon(corner, boundary[0]);

            if (result != Clipper2Lib::PointInPolygonResult::IsOutside) {
                is_rect_inside_polygon = true;
                bool has_collision = paths_intersect(paths, boundary);


                
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
        // patterns_to_cut.push_back(paths);
        if (num_corners_in_polygon == paths[0].size()){
            patterns_to_keep.push_back(paths);
        }else if (clip_boundaries){
            if (paths_intersect(paths, boundary)){
                patterns_to_cut.push_back(paths);
            }
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

    // Rescale
    Eigen::Vector2d min_coeff = target_uv.colwise().minCoeff(); // Find min and max values for normalization
    Eigen::Vector2d max_coeff = target_uv.colwise().maxCoeff();
    Eigen::Vector2d size = max_coeff - min_coeff; // Compute the size of the bounding box    
    target_uv.col(0) = target_uv.col(0).array() - min_coeff(0); // Translate UV coordinates so minimum is at the origin
    target_uv.col(1) = target_uv.col(1).array() - min_coeff(1);
    double scale_factor = 1.0 / std::max(size(0), size(1)); // Scale to fit in a 0-1 box while maintaining aspect ratio
    target_uv *= scale_factor;

    // Clip the pattern
    auto [clipped_pattern_v, clipped_pattern_f] = eigen_to_clipper(target_uv, target_f, pattern_v, pattern_f, clip_boundaries);

    // return std::make_tuple(clipped_pattern_v, clipped_pattern_f); // Comment this out to see 2d cropped pattern

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