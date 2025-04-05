********************************************************************************
Style
********************************************************************************

Python Code
===========

Use the compas style guide from the official documentation `documentation <https://compas.dev/compas/latest/devguide/code.html>`_.


C++ Code
========

* Functions: ``snake_case``
* Variables (local and public): ``snake_case``
* Private members: ``_snake_case`` (prefix with _)
* Static members: ``s_snake_case`` (prefix with s and _)
* Constants: ``SNAKE_UPPER_CASE``
* Class/Struct names: ``UpperCamelCase``

Namespaces
----------

.. code-block:: cpp

    // Do not use "using namespace std", specify namespace explicitly
    std::vector<double> points;

    // Do not use "using namespace Eigen", specify namespace explicitly
    Eigen::MatrixXd vertices;

Functions
---------

.. code-block:: cpp

    // Next line bracket style
    void compute_geodesic_distance()
    {
        /* content */
    }

    // Always include Windows-specific handling when needed
    #ifdef _WIN32
    #define NOMINMAX  // Prevent Windows max/min macro conflicts
    #endif

Structures
----------

.. code-block:: cpp

    // Structure name uses UpperCamelCase
    struct MeshData
    {
        // Structure attribute uses snake_case
        const char* file_name;
        Eigen::MatrixXd vertices;
        Eigen::MatrixXi faces;
    };


Classes
-------

.. code-block:: cpp

    // Class name uses UpperCamelCase
    class GeodesicSolver
    {
    public:
        GeodesicSolver(const double& tolerance);
        virtual ~GeodesicSolver();

        // Member functions use snake_case
        void compute_distance()
        {
            // Local variable uses snake_case
            double tolerance = 0.001;
        }

    // Field indicator to separate functions and attributes
    public:
        int result_count;      // Public member uses snake_case

    private:
        void validate_mesh();  // Private function uses snake_case
        double _tolerance;     // Private member uses _snake_case
        static int s_meshes;   // Static member uses s_snake_case
        const int MAX_COUNT = 100;  // Constant uses SNAKE_UPPER_CASE
    };

Docstrings
==========

Use Doxygen-style comments with the following format:

Functions and Methods
---------------------

.. code-block:: cpp

    /**
     * @brief Short description of function
     * @param[in] vertices Input mesh vertices (n x 3)
     * @param[in] faces Input mesh faces (m x 3)
     * @param[in] source_vertex Index of source vertex
     * @return Tuple containing distance field and geodesic path
     * @throws std::runtime_error if mesh is not manifold
     */
    std::tuple<Eigen::VectorXd, std::vector<int>> 
    compute_geodesic(const Eigen::MatrixXd& vertices, 
                    const Eigen::MatrixXi& faces,
                    int source_vertex);

Classes
-------

.. code-block:: cpp

    /**
     * @brief Solver for geodesic distance computation
     * @details Implements both exact and heat method approaches
     */
    class GeodesicSolver {
    public:
        /**
         * @brief Constructor for geodesic solver
         * @param method Method to use ("exact" or "heat")
         * @param tolerance Computation tolerance
         */
        GeodesicSolver(const std::string& method, double tolerance);
    };

Member Variables
----------------

.. code-block:: cpp

    class GeodesicSolver {
    private:
        double _tolerance;  //!< Tolerance for geodesic computation
        std::string _method;  //!< Method used ("exact" or "heat")
    };
