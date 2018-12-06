#include <igl/read_triangle_mesh.h>
#include <igl/hessian_energy.h>
#include <igl/massmatrix.h>
#include <igl/cotmatrix.h>
#include <igl/jet.h>
#include <igl/edges.h>
#include <igl/vertex_components.h>
#include <igl/remove_unreferenced.h>
#include <igl/opengl/glfw/Viewer.h>

#include <Eigen/Core>
#include <Eigen/SparseCholesky>

#include <iostream>
#include <set>
#include <limits>
#include <stdlib.h>

#include "tutorial_shared_path.h"

#include <igl/isolines.h>


int main(int argc, char * argv[])
{
    typedef Eigen::SparseMatrix<double> SparseMat;

    //Read our mesh
    Eigen::MatrixXd V;
    Eigen::MatrixXi F, E;
    if(!igl::read_triangle_mesh(
        argc>1?argv[1]: TUTORIAL_SHARED_PATH "/beetle.off",V,F)) {
        std::cout << "Failed to load mesh." << std::endl;
    }
    igl::edges(F,E);

    //Constructing an exact function to smooth
    Eigen::VectorXd zexact = V.block(0,2,V.rows(),1).array()
        + 0.5*V.block(0,1,V.rows(),1).array()
        + V.block(0,1,V.rows(),1).array().pow(2)
        + V.block(0,2,V.rows(),1).array().pow(3);

    //Make the exact function noisy
    srand(5);
    const double s = 0.2*(zexact.maxCoeff() - zexact.minCoeff());
    Eigen::VectorXd znoisy = zexact + s*Eigen::VectorXd::Random(zexact.size());

    //Constructing the squared Laplacian and squared Hessian energy
    SparseMat L, M;
    igl::cotmatrix(V, F, L);
    igl::massmatrix(V, F, igl::MASSMATRIX_TYPE_BARYCENTRIC, M);
    Eigen::SimplicialLDLT<SparseMat> solver(M);
    SparseMat MinvL = solver.solve(L);
    SparseMat QL = L.transpose()*MinvL;
    SparseMat QH;
    igl::hessian_energy(V, F, QH);

    //Solve to find Laplacian-smoothed and Hessian-smoothed solutions
    const double al = 8e-4;
    Eigen::SimplicialLDLT<SparseMat> lapSolver(al*QL + (1.-al)*M);
    Eigen::VectorXd zl = lapSolver.solve(al*M*znoisy);
    const double ah = 5e-6;
    Eigen::SimplicialLDLT<SparseMat> hessSolver(ah*QH + (1.-ah)*M);
    Eigen::VectorXd zh = hessSolver.solve(ah*M*znoisy);

    return 0;
}
