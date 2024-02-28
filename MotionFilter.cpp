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

    //inputs 
    string input = "C:/Users/aram_/Downloads/humanwalking.mp4";
    //string input = "C:/Users/aram_/Downloads/timelapse.mp4";
    //string input = "C:/Users/aram_/Downloads/sixseconds.mp4";

    //VideoCapture capture(0);
    VideoCapture capture(input);

    if (!capture.isOpened()) { //error in opening the video input
        cerr << "Unable to open: " << input << endl;
        return 0;
    }

    //Mats
    Mat oldframe, newframe, result, result2;
    Mat gray_res, thresh_res;

    // Frame/time variables
    int count = 0;
    double duration = 0;
    int skipFrames = 2;
    int frameCount = 0;
    int resize_val = 4;

    // Kernels, they can be MORPH_RECT, MORPH_CROSS, MORPH_ELLIPSE
    Mat kernel1 = getStructuringElement(MORPH_CROSS, Size(1, 1));
    Mat kernel3 = getStructuringElement(MORPH_CROSS, Size(3, 3)); 
    Mat kernel5 = getStructuringElement(MORPH_CROSS, Size(5, 5)); 

    // for connectedComponentsWithStats()
    vector<Rect> filtered_rects;
    vector<vector<Point>> components;
    Mat labels, stats, centroids;

    namedWindow("Result", 0);
    namedWindow("Original", 0);
    namedWindow("Thresh", 0);

    capture >> oldframe;
    resize(oldframe, oldframe, cv::Size(oldframe.cols / resize_val, oldframe.rows / resize_val));

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

        resize(newframe, newframe, cv::Size(newframe.cols / resize_val, newframe.rows / resize_val));
        absdiff(oldframe, newframe, result);

        cvtColor(result, gray_res, COLOR_BGR2GRAY);

        erode(result, result, kernel1, Point(-1, -1), 1);
        dilate(result, result, kernel3, Point(-1, -1), 1);

        //ADAPTIVE_THRESH_MEAN_C
        adaptiveThreshold(gray_res, thresh_res, 255, ADAPTIVE_THRESH_GAUSSIAN_C, THRESH_BINARY_INV, 9, 5.5);
        imshow("Thresh", thresh_res);

        int connected_components = connectedComponentsWithStats(thresh_res, labels, stats, centroids, 8, CV_32S); //connectivity can be 4 or 8
        for (int i = 1; i < connected_components; i++) { // Skip background (label 0)
            int area = stats.at<int>(i, CC_STAT_AREA);
            if (area > 100 && area < 750) { // Adjust threshold based on image complexity
                Rect rect(stats.at<int>(i, CC_STAT_LEFT),
                          stats.at<int>(i, CC_STAT_TOP),
                          stats.at<int>(i, CC_STAT_WIDTH),
                          stats.at<int>(i, CC_STAT_HEIGHT));
                filtered_rects.push_back(rect);
            }
        }

        // Draw rectangles
        for (const auto& rect : filtered_rects) {
            rectangle(result, rect.tl(), rect.br(), Scalar(0, 255, 0), 1);
        }

        imshow("Result", result * 1.5);
        oldframe = newframe.clone();
        filtered_rects.clear();

        auto now = chrono::system_clock::now();

        chrono::duration<double> elapsed_seconds = now - then;
        cout << "Time elapsed: " << elapsed_seconds.count() << " seconds" << endl;

        count++;
        duration += elapsed_seconds.count();

        int keyboard = waitKey(2);
        if (keyboard == 'q' || keyboard == 27)
            break;

    }

    cout << endl << "Average fps?: " << count / duration << endl;
    cout << endl << "Average proccessing time: " << duration / count << endl << endl;
    
    return 0;
}


