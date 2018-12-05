#include <Eigen/Core>
#include <Eigen/Dense>
#include <Eigen/Sparse>

namespace compas
{
	Eigen::MatrixXd ArrayToMatrixXd(double **array, int m, int n)
	{
		int i, j;

	    Eigen::MatrixXd M(m, n);

	    for (i = 0; i < m; i++) {
	    	for (j = 0; j < n; j++) {
	    		M(i, j) = array[i][j];
	    	}
	    }

		return M;
	}

	Eigen::MatrixXi ArrayToMatrixXi(int **array, int m, int n)
	{
		int i, j;

	    Eigen::MatrixXi M(m, n);

	    for (i = 0; i < m; i++) {
	    	for (j = 0; j < n; j++) {
	    		M(i, j) = array[i][j];
	    	}
	    }

		return M;
}
}
