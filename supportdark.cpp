#include "supportdark.h"
#include <iostream>

using namespace cv;
using namespace std;

CHazeRemoval::CHazeRemoval() {
	rows = 0;
	cols = 0;
	channels = 0;
}

CHazeRemoval::~CHazeRemoval() {

}

bool CHazeRemoval::InitProc(int width, int height, int nChannels) {
	bool ret = false;
	rows = height;
	cols = width;
	channels = nChannels;

	if (width > 0 && height > 0 && nChannels == 3) ret = true;
	return ret;
}

bool CHazeRemoval::Process(const unsigned char* indata, unsigned char* outdata, int width, int height, int nChannels) {
	bool ret = true;
	if (!indata || !outdata) {
		ret = false;
	}
	rows = height;
	cols = width;
	channels = nChannels;

	int radius = 7;
	vector<Pixel> tmp_vec;
	Mat * p_src = new Mat(rows, cols, CV_8UC3, (void *)indata);
	Mat * p_dark = new Mat(rows, cols, CV_64FC1);

	get_dark_channel(p_src, tmp_vec, rows, cols, channels, radius, p_dark);

    assign_data(outdata, p_dark, rows, cols, 1);

	return ret;
}

/* bool sort_fun(const Pixel&a, const Pixel&b) {
	return a.val > b.val;
} */

void get_dark_channel(const cv::Mat *p_src, std::vector<Pixel> &tmp_vec, int rows, int cols, int channels, int radius, cv::Mat *p_dark) {
	for (int i = 0; i < rows; i++) {
		for (int j = 0; j < cols; j++) {
			int rmin = cv::max(0, i - radius);
			int rmax = cv::min(i + radius, rows - 1);
			int cmin = cv::max(0, j - radius);
			int cmax = cv::min(j + radius, cols - 1);
			double min_val = 255;
			for (int x = rmin; x <= rmax; x++) {
				for (int y = cmin; y <= cmax; y++) {
					cv::Vec3b tmp = p_src->ptr<cv::Vec3b>(x)[y];
					uchar b = tmp[0];
					uchar g = tmp[1];
					uchar r = tmp[2];
					uchar minpixel = b > g ? ((g>r) ? r : g) : ((b > r) ? r : b);
					min_val = cv::min((double)minpixel, min_val);
				}
			}
			p_dark->ptr<double>(i)[j] = min_val;
			/* tmp_vec.push_back(Pixel(i, j, uchar(min_val))); */
		}
	}
	/* std::sort(tmp_vec.begin(), tmp_vec.end(), sort_fun); */
}

void assign_data(unsigned char *outdata, const cv::Mat *p_dark, int rows, int cols, int channels) {
	for (int i = 0; i < rows*cols*channels; i++) {
		*(outdata + i) = (unsigned char)(*((double*)(p_dark->data) + i));
	}
}