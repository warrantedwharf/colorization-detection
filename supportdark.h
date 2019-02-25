#ifndef SUPPORT_DARK_H
#define SUPPORT_DARK_H

#include "opencv2/opencv.hpp"
#include <vector>

typedef struct _pixel {
	int i;
	int j;
	uchar val;
	_pixel(int _i, int _j, uchar _val) :i(_i), j(_j), val((uchar)_val) {}
} Pixel;

class CHazeRemoval
{
public:
	CHazeRemoval();
	~CHazeRemoval();

public:
	bool InitProc(int width, int height, int nChannels);
	bool Process(const unsigned char* indata, unsigned char* outdata, unsigned char* outdatb, int width, int height, int nChannels);

private:
	int rows;
	int cols;
	int channels;

};

void get_dark_channel(const cv::Mat *p_src, std::vector<Pixel> &tmp_vec, int rows, int cols, int channels, int radius,  cv::Mat *p_dark, cv::Mat *p_bright);

void assign_data(unsigned char *outdata, unsigned char *outdatb, const cv::Mat *p_dark, const cv::Mat *p_bright, int rows, int cols, int channels);



#endif // !SUPPORT_DARK_H