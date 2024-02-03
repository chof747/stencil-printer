/*
difference() {
	cube([45,55,.3]);
 	}
}
*/

stencil_height = 0.6;
dxf_file = "wlan-thermo-front-panel-F_Paste.dxf";

minkowski() {
  
  linear_extrude(stencil_height) import(dxf_file);
}