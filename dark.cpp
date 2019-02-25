#include "supportdark.h"
#include "opencv2/opencv.hpp"
#include <iostream>

using namespace cv;
using namespace std;

int main(int argc, char **args) {
	const char * img_path = args[1];
	const char * dark_path = args[2];
	const char * bright_path = args[3];
	cout<<bright_path;
	Mat in_img = imread(img_path);
    Mat out_img(in_img.rows, in_img.cols, CV_8UC1);
	Mat out_imh(in_img.rows, in_img.cols, CV_8UC1);
	unsigned char * indata = in_img.data;
	unsigned char * outdata = out_img.data;
	unsigned char * outdatb = out_imh.data;

    CHazeRemoval hr;
	cout << hr.InitProc(in_img.cols, in_img.rows, in_img.channels()) << endl;
	cout << hr.Process(indata, outdata, outdatb, in_img.cols, in_img.rows, in_img.channels()) << endl;
	imwrite(dark_path, out_img);
	imwrite(bright_path, out_imh);
	/* imshow("out_img", out_img); */
	waitKey(0);

    //code ends here
    return 0;

}    