scaling=1;
board_y = 10;
board_x = 12;
board_length = board_y*scaling;
board_width = board_x*scaling;
rim = 5;
stencil_height = 0.3;
bottom_height  = 1.5;
board_height = 1.6;
tolerance = 0.1;
round_corners = 1;
board_outline = "wlan-thermo-front-panel-F_Paste.dxf";

smaller_edge=min(board_width, board_length);
total_height=board_height + tolerance + stencil_height;
bottom_distance =  bottom_height - 0.001;

ejection_sphere_radius= smaller_edge;
ring_radius= smaller_edge/2 + rim/2;
z_offset = ejection_sphere_radius * (1 - sqrt(1-pow(ring_radius/ejection_sphere_radius,2)));

$fn=30;

union() {
cylinder(total_height + bottom_height, 1);
translate([board_width+rim*2, 0, 0]) 
  cylinder(total_height + bottom_height, 1);
translate([0, board_length+rim*2, 0])
  cylinder(total_height + bottom_height, 1);
translate([board_width+rim*2, board_length+rim*2, 0])
  cylinder(total_height + bottom_height, 1);

translate([0,-1,0]) 
  cube([board_width+rim*2,2,total_height + bottom_height]);
translate([0,board_length+rim*2 - 1,0]) 
  cube([board_width+rim*2,2,total_height + bottom_height]);
translate([-1,0,0])
  cube([2,board_length+rim*2,total_height + bottom_height]);
translate([board_width+rim*2-1,0,0])
  cube([2,board_length+rim*2,total_height + bottom_height]);

translate([0,0,bottom_distance])
  union() {
    difference() {
      difference() {

        cube([board_width+rim*2, board_length+rim*2, total_height]);
          translate([rim,rim,-tolerance]) minkowski() {
          scale([scaling,scaling,1])
          linear_extrude(stencil_height + board_height + tolerance + 0.1) import(board_outline);
          cube(tolerance);
          };
      };

      
      translate([board_width/2+rim, board_length/2+rim, ejection_sphere_radius + total_height -  z_offset + tolerance])
        sphere(ejection_sphere_radius);  
      
    };
      translate([0,0, -1 * bottom_distance])
        cube([board_width+rim*2, board_length+rim*2, bottom_height]);
  };
  
  /*
  
  minkowski() {
          scale([scaling,scaling,1])
          linear_extrude(stencil_height + board_height + tolerance + 0.1) import(board_outline);
          cube(tolerance);
          };
          */
};