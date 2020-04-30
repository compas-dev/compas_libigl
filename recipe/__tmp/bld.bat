$PYTHON -m pip install . -vv
mkdir $SP_DIR/compas_libigl/booleans
mkdir $SP_DIR/compas_libigl/geodistance
mkdir $SP_DIR/compas_libigl/isolines
mkdir $SP_DIR/compas_libigl/planarize
mkdir $SP_DIR/compas_libigl/triangulation
copy $RECIPE_DIR/../modules/booleans/__init__.py $SP_DIR/compas_libigl/booleans/__init__.py
copy $RECIPE_DIR/../modules/geodistance/__init__.py $SP_DIR/compas_libigl/geodistance/__init__.py
copy $RECIPE_DIR/../modules/isolines/__init__.py $SP_DIR/compas_libigl/isolines/__init__.py
copy $RECIPE_DIR/../modules/planarize/__init__.py $SP_DIR/compas_libigl/planarize/__init__.py
copy $RECIPE_DIR/../modules/triangulation/__init__.py $SP_DIR/compas_libigl/triangulation/__init__.py
