File.openSequence("/home/gianthk/Data/2019.001.coop_TUberlin_simulierte_Mensch.iorig/trabecular_sample_mini2/");
setAutoThreshold("Otsu dark");
//run("Threshold...");
setOption("BlackBackground", false);
run("Convert to Mask", "method=Otsu background=Dark");
run("Image Sequence... ", "select=/home/gianthk/Data/2019.001.coop_TUberlin_simulierte_Mensch.iorig/trabecular_sample_mini2_bin/ dir=/home/gianthk/Data/2019.001.coop_TUberlin_simulierte_Mensch.iorig/trabecular_sample_mini2_bin/ format=TIFF name=2000L_crop_imgaussfilt_60micron_uint8_");
close();