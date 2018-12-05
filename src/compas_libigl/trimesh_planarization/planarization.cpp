#include <Eigen/Core>
#include <Eigen/Dense>

#include <igl/planarize_quad_mesh.h>

#include "../../../include/compas/utilities.h"


extern "C" int planarize(double **vertices, int v, int **faces, int f, int kmax, double d);


int planarize(double **vertices, int v, int **faces, int f, int kmax, double d)
{
    using namespace Eigen;

    int i;

    MatrixXd V = compas::ArrayToMatrixXd(vertices, v, 3);
    MatrixXi F = compas::ArrayToMatrixXi(faces, f, 4);

    MatrixXd Vplanar(v, 3);

    igl::planarize_quad_mesh(V, F, kmax, d, Vplanar);

    for (i = 0; i < v; i++) {
        vertices[i][0] = Vplanar(i, 0);
        vertices[i][1] = Vplanar(i, 1);
        vertices[i][2] = Vplanar(i, 2);
    }

    return 0;
}
