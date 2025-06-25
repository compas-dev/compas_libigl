#include "mapping.hpp"

// Custom hash function for tuple
struct TupleHash {
    std::size_t operator()(const std::tuple<int64_t, int64_t>& t) const {
        auto h1 = std::hash<int64_t>{}(std::get<0>(t));
        auto h2 = std::hash<int64_t>{}(std::get<1>(t));
        return h1 ^ (h2 << 1); // basic hash combination
    }
};

std::tuple<int64_t, int64_t> grid_key(double x, double y, double tolerance) {
    double cell_size = tolerance * 10.0;
    return {
        static_cast<int64_t>(std::floor(x / cell_size)),
        static_cast<int64_t>(std::floor(y / cell_size))
    };
}

bool is_same_point(double x1, double y1, double x2, double y2, double tol) {
    double dx = x1 - x2;
    double dy = y1 - y2;
    return (dx*dx + dy*dy) < (tol*tol);
}

compas::VectorVectorInt map_mesh_cropped(
    Eigen::Ref<const compas::RowMatrixXd> v, 
    Eigen::Ref<const compas::RowMatrixXi> f, 
    Eigen::Ref<const compas::RowMatrixXd> uv,
    Eigen::Ref<compas::RowMatrixXd> pattern_v, 
    const compas::VectorVectorInt& pattern_f, 
    Eigen::Ref<const compas::RowMatrixXd> pattern_uv,
    Eigen::Ref<compas::RowMatrixXd> pattern_normals)
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

    // Compute per-vertex normals for the target mesh
    Eigen::MatrixXd v_normals;
    igl::per_vertex_normals(v, f, v_normals);
    
    // Ensure normals matrix has correct dimensions
    if (pattern_normals.rows() != pattern_v.rows()) {
        // Resize normals matrix to match pattern vertices
        pattern_normals.resize(pattern_v.rows(), 3);
    }
    
    // Always compute normals
    bool compute_normals = true;
       
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
        
        // Update pattern vertex position through barycentric interpolation, comment this out if you keep 2D pattern
        pattern_v.row(id) = A * L(0, 0) + B * L(0, 1) + C * L(0, 2);
        
        // If normals are requested, interpolate them using the same barycentric coordinates
        if (compute_normals) {
            // Get vertex normals for the triangle vertices
            Eigen::MatrixXd NA(1, 3), NB(1, 3), NC(1, 3);
            NA << v_normals(f(faceID, 0), 0), v_normals(f(faceID, 0), 1), v_normals(f(faceID, 0), 2);
            NB << v_normals(f(faceID, 1), 0), v_normals(f(faceID, 1), 1), v_normals(f(faceID, 1), 2);
            NC << v_normals(f(faceID, 2), 0), v_normals(f(faceID, 2), 1), v_normals(f(faceID, 2), 2);
            
            // Interpolate normal using barycentric coordinates
            Eigen::MatrixXd interpolated_normal = NA * L(0, 0) + NB * L(0, 1) + NC * L(0, 2);
            
            // Normalize the interpolated normal
            double norm = interpolated_normal.norm();
            if (norm > 1e-10) { // Avoid division by very small numbers
                interpolated_normal /= norm;
            }
            
            pattern_normals.row(id) = interpolated_normal;
        }
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




std::tuple<compas::RowMatrixXd, std::vector<std::vector<int>>, std::vector<bool>, std::vector<int>> eigen_to_clipper (
    Eigen::Ref<const compas::RowMatrixXd> flattned_target_uv,
    Eigen::Ref<const compas::RowMatrixXi> target_f, 
    
    Eigen::Ref<const compas::RowMatrixXd> pattern_v, 
    const std::vector<std::vector<int>>& pattern_f,
    bool clip_boundaries,
    bool simplify_borders,
    std::vector<int>& fixed_vertices,
    double tolerance
)   
{

    ////////////////////////////////////////////////////////////////////////////////////////
    // Fixed points
    ////////////////////////////////////////////////////////////////////////////////////////
    Clipper2Lib::PathD fixed;
    for (const auto &point_id : fixed_vertices){
        fixed.emplace_back(Clipper2Lib::PointD(flattned_target_uv(point_id, 0), flattned_target_uv(point_id, 1)));
    }
 
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

        if (!clip_boundaries){
            patterns_to_keep.push_back(paths);
            continue;
        }

        // Get bounds of current pattern polygon
        Clipper2Lib::RectD pattern_bounds = Clipper2Lib::GetBounds(paths);
        
        // Check if the pattern bounds intersect with boundary bounds
        if (!pattern_bounds.Intersects(boundary_bounds))
            continue;
    
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

        // Rare case, but polygon can be bigger than a hole:
        bool is_hole_in_polygon = false;
        for (size_t i = 1; i < boundary.size(); i++) {    
            Clipper2Lib::PathD path = boundary[i];
            for (const auto& corner : path) {
                auto result = Clipper2Lib::PointInPolygon(corner, paths[0]);
                if (result != Clipper2Lib::PointInPolygonResult::IsOutside) {
                    is_hole_in_polygon = true;
                    break;
                }
            }
        }

        // Fully enclosed polygons are added to the keep list
        // Other polygons edges are intersected with the boundary

        if (num_corners_in_polygon == paths[0].size() && !is_hole_in_polygon){ //  
            patterns_to_keep.push_back(paths);
        }else if(num_corners_in_polygon > 0 || paths_intersect(paths, boundary) || is_hole_in_polygon){
            patterns_to_cut.push_back(paths);
        }



    }

    // perform intersection
    std::vector<Clipper2Lib::PathsD> solutions;
    for (const auto &subject : patterns_to_cut){
        Clipper2Lib::PathsD solution = Clipper2Lib::Intersect(subject, boundary, Clipper2Lib::FillRule::NonZero, 8);

        if (solution.size() == 0){
            // If no intersection is found, skip this polygon
            continue;
        }else if (solution.size() > 1 || !simplify_borders){
            // Highly likely we do not consider polygons with holes, we do not simplify them.
            solutions.push_back(solution);
        }else{
            // After boolean intersection the pattern is merged with boundary polygons. This is often not wanted.
            // Simplification is made by comparing polygon after boolean intersection and before. If the points lie on the initial polygon edges we keep them.
            // Additionally we add an option to keep arbitrary points from a user given points or boundary valence points.
            Clipper2Lib::PathsD simplified_paths{Clipper2Lib::PathD()};
            simplified_paths[0].reserve(subject[0].size());

            for (const auto &p : solution[0]){ // iterate the points of the intersection polygon
                
                // First check if point is close to any vertex (corner)
                bool point_added = false;
                for(size_t i = 0; i < subject[0].size(); i++){
                    double dx = p.x - subject[0][i].x;
                    double dy = p.y - subject[0][i].y;
                    if (dx*dx + dy*dy < tolerance*tolerance){
                        simplified_paths[0].push_back(p);
                        point_added = true;
                        break;
                    }
                }

                // Check if point is close to any fixed point
                for(size_t i = 0; i < fixed.size(); i++){
                    double fx = fixed[i].x;
                    double fy = fixed[i].y;
                    double dx = p.x - fx;
                    double dy = p.y - fy;
                    if (dx*dx + dy*dy < tolerance*tolerance){
                        simplified_paths[0].push_back(p);
                        point_added = true;
                        break;
                    }
                }
                
                // If not close to a vertex, check if close to any edge
                if (!point_added) {
                    for(size_t i = 0; i < subject[0].size()-1; i++){
                        if (Clipper2Lib::PerpendicDistFromLineSqrd(p, subject[0][i], subject[0][i+1]) < tolerance*tolerance){
                            simplified_paths[0].push_back(p);
                            break;
                        }
                    }
                    // Also check the closing edge between last and first point
                    if (subject[0].size() > 1){
                        size_t last = subject[0].size()-1;
                        if (Clipper2Lib::PerpendicDistFromLineSqrd(p, subject[0][last], subject[0][0]) < tolerance*tolerance){
                            simplified_paths[0].push_back(p);
                        }
                    }
                }
                }

            if (simplified_paths[0].size() > 2)
                solutions.push_back(simplified_paths);
        }
        

    }

    std::vector<std::array<double, 3>> unique_points;
    std::unordered_map<std::tuple<int64_t, int64_t>, std::vector<int>, TupleHash> grid_map;
    std::vector<std::vector<int>> faces;
    std::vector<int> groups;
    std::vector<bool> is_boundary; 
    faces.reserve(solutions.size() + patterns_to_keep.size());
    groups.reserve(solutions.size() + patterns_to_keep.size());
    is_boundary.reserve(solutions.size() + patterns_to_keep.size());
    
    // 9 bucket search to avoid rounding wrong rounded grid key, when the distance is close to the tolerance.
    auto find_or_add_point = [&](double x, double y) -> int {
        double z = 0.0;
        
        // Get the base grid key for this point
        auto base_key = grid_key(x, y, tolerance);
        
        // Check the point's own cell and all neighboring cells
        for (int di = -1; di <= 1; ++di) {
            for (int dj = -1; dj <= 1; ++dj) {
                // Create the neighboring grid key
                auto neighbor_key = std::make_tuple(std::get<0>(base_key) + di, std::get<1>(base_key) + dj);
                
                // Check if this neighboring cell exists in our grid map
                auto grid_it = grid_map.find(neighbor_key);
                if (grid_it != grid_map.end()) {
                    // Check all points in this cell
                    for (int idx : grid_it->second) {
                        const auto& pt = unique_points[idx];
                        if (is_same_point(pt[0], pt[1], x, y, tolerance))
                            return idx;
                    }
                }
            }
        }
        
        // If we get here, the point doesn't exist yet
        // Add it to the grid using the base key
        int new_index = static_cast<int>(unique_points.size());
        unique_points.push_back({x, y, z});
        grid_map[base_key].push_back(new_index);
        return new_index;
    };

    int group_id = 0;
    for (const auto &solution : solutions) {
        for (const auto& path : solution) {
            std::vector<int> face;
            for (const auto& point : path) {
                int idx = find_or_add_point(point.x, point.y);
                face.push_back(idx);
            }
            faces.push_back(face);
            groups.push_back(group_id);
            is_boundary.push_back(true);
        }
        group_id++;
    }
    
    for (const auto &subject : patterns_to_keep) {
        for (const auto& path : subject) {
            std::vector<int> face;
            for (const auto& point : path) {
                int idx = find_or_add_point(point.x, point.y);
                face.push_back(idx);
            }
            faces.push_back(face);
            groups.push_back(group_id);
            is_boundary.push_back(false);
        }
        group_id++;
    }

    compas::RowMatrixXd vertices(unique_points.size(), 3);
    for (size_t i = 0; i < unique_points.size(); ++i) {
        vertices(i, 0) = unique_points[i][0];
        vertices(i, 1) = unique_points[i][1];
        vertices(i, 2) = 0.0;
    }

    return std::make_tuple(vertices, faces, is_boundary, groups);

}


compas::MeshMapResult map_mesh_with_automatic_parameterization(
    Eigen::Ref<const compas::RowMatrixXd> target_v, 
    Eigen::Ref<const compas::RowMatrixXi> target_f, 
    Eigen::Ref<compas::RowMatrixXd> pattern_v, 
    const compas::VectorVectorInt& pattern_f,
    bool clip_boundaries,
    bool simplify_borders,
    compas::VectorInt& fixed_vertices,
    double tolerance)
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
    auto [clipped_pattern_v, clipped_pattern_f, clipped_pattern_is_boundary, clipped_pattern_groups] = eigen_to_clipper(target_uv, target_f, pattern_v, pattern_f, clip_boundaries, simplify_borders, fixed_vertices, tolerance);

    Eigen::MatrixXd clipped_pattern_uv;
    clipped_pattern_uv.setZero();
    clipped_pattern_uv = clipped_pattern_v.leftCols(2);

    // Initialize normals matrix for pattern vertices
    compas::RowMatrixXd pattern_normals;
    pattern_normals.resize(clipped_pattern_v.rows(), 3);
    
    // Map the mesh with normal mapping
    auto result = map_mesh_cropped(
        target_v, 
        target_f,
        target_uv,
        clipped_pattern_v,
        clipped_pattern_f,
        clipped_pattern_uv,
        pattern_normals);

    return std::make_tuple(clipped_pattern_v, result, pattern_normals, clipped_pattern_is_boundary, clipped_pattern_groups);

}

// Define the nanobind module at global scope
NB_MODULE(_mapping, m)
{
    m.def(
        "map_mesh_with_automatic_parameterization",
        &map_mesh_with_automatic_parameterization,
        "Map a 2D pattern mesh onto a 3D target mesh with automatic parameterization, returning vertices, faces and normal vectors.",
        "target_v"_a,
        "target_f"_a,
        "pattern_v"_a,
        "pattern_f"_a,
        "clip_boundaries"_a,
        "simplify_borders"_a,
        "fixed_vertices"_a,
        "tolerance"_a
    );
}