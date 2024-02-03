board_length = 50;
board_width = 70;
stencil_height = 0.3;
board_height = 1.6;
tolerance = 0.1;

difference() {
  cube([board_width, board_length, stencil_height + board_height]);
  	translate([1.5,3,-0.1]) minkowski() {
		linear_extrude(stencil_height + board_height + tolerance) import("wlan-thermo-front-panel-Edge_Cuts.dxf");
		cube(tolerance);
    };
}