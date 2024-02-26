#include <iostream>
#include <sstream>
#include <string>
#include <chrono>
#include <opencv2/core.hpp>
#include <opencv2/imgcodecs.hpp>
#include <opencv2/imgproc.hpp>
#include <opencv2/videoio.hpp>
#include <opencv2/highgui.hpp>
#include <opencv2/video.hpp>
#include <opencv2/bgsegm.hpp>
#include <opencv2/features2d.hpp>

using namespace std;
using namespace cv;

int main() {

    string input = "C:/Users/aram_/Downloads/humanwalking.mp4";
    //string input = "C:/Users/aram_/Downloads/timelapse.mp4";
    //string input = "C:/Users/aram_/Downloads/sixseconds.mp4";

    //VideoCapture capture(0);
    VideoCapture capture(input);

    if (!capture.isOpened()) { //error in opening the video input
        cerr << "Unable to open: " << input << endl;
        return 0;
    }

    Mat oldframe, newframe, result, result2;
    Mat gray_res, thresh_res;

    int count = 0;
    double duration = 0;
    int skipFrames = 2;
    int frameCount = 0;

    Mat kernel1 = getStructuringElement(MORPH_RECT, Size(1, 1));
    Mat kernel3 = getStructuringElement(MORPH_RECT, Size(3, 3)); // MORPH_RECT, MORPH_CROSS, MORPH_ELLIPSE
    Mat kernel5 = getStructuringElement(MORPH_RECT, Size(5, 5)); 
    Mat kernel11 = Mat::zeros(11, 11, CV_8UC1);

    // Set the border values to 1
    for (int i = 0; i < 11; ++i) {
        kernel11.at<uchar>(0, i) = 1; // Top row
        kernel11.at<uchar>(11 - 1, i) = 1; // Bottom row
        kernel11.at<uchar>(i, 0) = 1; // Leftmost column
        kernel11.at<uchar>(i, 11 - 1) = 1; // Rightmost column
    }

    namedWindow("Result", 0);
    namedWindow("Original", 0);
    namedWindow("Thresh", 0);

    capture >> oldframe;
    resize(oldframe, oldframe, cv::Size(oldframe.cols / 3, oldframe.rows / 3));

    vector<Rect> filtered_rects;
    vector<vector<Point>> components;
    Mat labels, stats, centroids;
    int max_rect_area_threshold = 850;


    while (true)
    {
        capture >> newframe;
        if (newframe.empty())
            break;
        imshow("Original", newframe);

        frameCount++;
        if (frameCount % skipFrames != 0)
            continue;

        auto then = chrono::system_clock::now();

        filtered_rects.clear();

        resize(newframe, newframe, cv::Size(newframe.cols / 3, newframe.rows / 3));
        absdiff(oldframe, newframe, result);

        cvtColor(result, gray_res, COLOR_BGR2GRAY);

        erode(result, result, kernel1, Point(-1, -1), 1);
        dilate(result, result, kernel3, Point(-1, -1), 1);

        //filter2D(result, result2, -1, kernel11);
        adaptiveThreshold(gray_res, thresh_res, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY_INV, 11, 5);
        imshow("Thresh", thresh_res);

        int connected_components = connectedComponentsWithStats(thresh_res, labels, stats, centroids, 4, CV_32S);
        for (int i = 1; i < connected_components; i++) { // Skip background (label 0)
            int area = stats.at<int>(i, CC_STAT_AREA);
            if (area > 200 && area < max_rect_area_threshold) { // Adjust threshold based on image complexity
                Rect rect(stats.at<int>(i, CC_STAT_LEFT),
                    stats.at<int>(i, CC_STAT_TOP),
                    stats.at<int>(i, CC_STAT_WIDTH),
                    stats.at<int>(i, CC_STAT_HEIGHT));
                filtered_rects.push_back(rect);
            }
        }

        // Draw rectangles
        for (const auto& rect : filtered_rects) {
            rectangle(result, rect.tl(), rect.br(), Scalar(0, 255, 0), 2);
        }

        imshow("Result", result * 2);
        oldframe = newframe.clone();

        auto now = chrono::system_clock::now();

        chrono::duration<double> elapsed_seconds = now - then;
        cout << "Time elapsed: " << elapsed_seconds.count() << " seconds" << endl;

        count++;
        duration += elapsed_seconds.count();

        int keyboard = waitKey(0);
        if (keyboard == 'q' || keyboard == 27)
            break;

    }

    cout << endl << "Average fps?: " << count / duration << endl;
    cout << endl << "Average proccessing time: " << duration / count << endl << endl;
    
    return 0;
}


