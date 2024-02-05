stencil_height = 0.6;
front_paste = "";
tolerance=0.1;

$fn=30;

minkowski() {
  linear_extrude(stencil_height) import(front_paste);
  //cube(tolerance);
};