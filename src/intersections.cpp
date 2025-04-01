#include "intersections.hpp"

/**
 * Compute intersection between a single ray and a mesh.
 * 
 * @param point Origin point of the ray
 * @param direction Direction vector of the ray
 * @param V #V x 3 matrix of vertex coordinates
 * @param F #F x 3 matrix of triangle indices
 * @return Vector of intersection hits, each containing (face_id, u, v, t) where:
 *         - face_id: index of intersected face
 *         - u, v: barycentric coordinates of hit point
 *         - t: ray parameter at intersection
 */
std::vector<std::tuple<int, float, float, float>>
intersection_ray_mesh(const Eigen::Vector3d& point, const Eigen::Vector3d& direction,
                     const compas::RowMatrixXd& V, const compas::RowMatrixXi& F) {
    std::vector<std::tuple<int, float, float, float>> hits;
    std::vector<igl::Hit<double>> igl_hits;

    bool result = igl::ray_mesh_intersect(point, direction, V, F, igl_hits);

    if (result) {
        for (const auto& hit : igl_hits) {
            hits.emplace_back(hit.id, hit.u, hit.v, hit.t);
        }
    }

    return hits;
}

/**
 * Compute intersections between multiple rays and a mesh.
 * 
 * @param points #R x 3 matrix of ray origin points
 * @param directions #R x 3 matrix of ray direction vectors
 * @param V #V x 3 matrix of vertex coordinates
 * @param F #F x 3 matrix of triangle indices
 * @return Vector of intersection hits per ray, each hit containing (face_id, u, v, t)
 */
std::vector<std::vector<std::tuple<int, float, float, float>>>
intersection_rays_mesh(const compas::RowMatrixXd& points,
                      const compas::RowMatrixXd& directions,
                      const compas::RowMatrixXd& V, 
                      const compas::RowMatrixXi& F) {
    std::vector<std::vector<std::tuple<int, float, float, float>>> hits_per_ray;
    hits_per_ray.reserve(points.rows());

    for (Eigen::Index i = 0; i < points.rows(); ++i) {
        std::vector<igl::Hit<double>> igl_hits;
        bool result = igl::ray_mesh_intersect(points.row(i), directions.row(i), V, F, igl_hits);

        std::vector<std::tuple<int, float, float, float>> hits;
        if (result) {
            hits.reserve(igl_hits.size());
            for (const auto& hit : igl_hits) {
                hits.emplace_back(hit.id, hit.u, hit.v, hit.t);
            }
        }
        hits_per_ray.push_back(std::move(hits));
    }

    return hits_per_ray;
}

NB_MODULE(_intersections, m) {
    m.doc() = "Ray-mesh intersection functions using libigl";

    m.def(
        "intersection_ray_mesh",
        &intersection_ray_mesh,
        "Compute intersection between a single ray and a mesh",
        "point"_a,
        "direction"_a,
        "V"_a,
        "F"_a
    );

    m.def(
        "intersection_rays_mesh",
        &intersection_rays_mesh,
        "Compute intersections between multiple rays and a mesh",
        "points"_a,
        "directions"_a,
        "V"_a,
        "F"_a
    );
}