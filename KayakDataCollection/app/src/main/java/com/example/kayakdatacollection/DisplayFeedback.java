package com.example.kayakdatacollection;

import android.content.Intent;
import android.os.Bundle;
import android.widget.ImageView;
import android.widget.TextView;

import androidx.appcompat.app.AppCompatActivity;

import java.util.HashMap;
import java.util.Map;

public class DisplayFeedback extends AppCompatActivity {
    Map<String, int[]> map = new HashMap<String, int[]>() {{
        put("A", new int[]{1, 0, 0, 63, 0});
        put("B", new int[]{0, 2, 1, 61, 0});
        put("C", new int[]{11, 2, 10, 59, 0});
        put("D", new int[]{0, 1, 1, 56, 0});
        put("E", new int[]{2, 0, 0, 56, 0});
        put("F", new int[]{0, 0, 3, 55, 0});
        put("G", new int[]{0, 0, 34, 26, 0});
        put("H", new int[]{0, 0, 7, 49, 0});
        put("A2", new int[]{39, 1, 0, 4, 0});
        put("B2", new int[]{36, 0, 4, 18, 0});
        put("C2", new int[]{44, 0, 2, 10, 0});
    }};
    int[] feedbackArray = map.get("B");
    String[] feedbackNames = new String[] {"Perfect","Over Reaching","Not Upright","Stroke Too Wide","Blade Angle"};

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.display_feedback);
        Intent intent = getIntent();

        double perfectPercent = calculatePerfectPercent();
        int imageToDisplay = getImageName(perfectPercent);
        ImageView rank = (ImageView) findViewById(R.id.rankImage);
        rank.setImageResource(imageToDisplay);

        ImageView correction = (ImageView) findViewById(R.id.correctionImage);
        String biggestError = calculateBiggestError();
        int correctionImage = getCorrectionImage(biggestError);
        correction.setImageResource(correctionImage);

        TextView textView = findViewById(R.id.textView);
        textView.setText(getRankUpSentance(perfectPercent) + biggestError + "\n\n" + getExplination(biggestError));
    }

    private double calculatePerfectPercent(){
        int total = 0;
        for (int i:feedbackArray) {
            total+= i;
        }
        return 100*((double)feedbackArray[0]/total);
    }

    private int getImageName(double perfectPercent){
        if(perfectPercent < 20){
            return R.drawable.tadpole;
        } else if(perfectPercent < 40){
            return R.drawable.salmon;
        } else if(perfectPercent < 60){
            return R.drawable.squid;
        } else if(perfectPercent < 80){
            return R.drawable.dolphin;
        }
        return R.drawable.shark;
    }

    private String getRankUpSentance(double perfectPercent){
        if(perfectPercent < 20){
            return "Like a Tadpole your journeys only just beginning \n" +
                    "To become a Salmon focus on ";
        } else if(perfectPercent < 40){
            return "Well done!  You are a Salmon! \n" +
                    "To become a Squid, focus on ";
        } else if(perfectPercent < 60){
            return "Congratulations, you are a Salmon!\n" +
                    " To become a Dolphin, focus on ";
        } else if(perfectPercent < 80){
            return "Great Job, you are a Dolphin! \n" +
                    "To become a Shark focus on ";
        }
        String r = "Fantastic! You are a Shark in the water!";
        if (perfectPercent < 100){
            r += "\nTo improve even more focus on ";
        }
        return r;
    }

    private String calculateBiggestError(){
        int max = 0;
        int maxI = 0;
        for (int i = 1; i < feedbackArray.length; i++) {
            if(feedbackArray[i]>max){
                max = feedbackArray[i];
                maxI = i;
            }
        }
        return feedbackNames[maxI];
    }

    private int getCorrectionImage(String errorName){
        if (errorName == feedbackNames[1]){
            return R.drawable.overreach;
        } else if (errorName == feedbackNames[2]){
            return R.drawable.notupright;
        } else if (errorName == feedbackNames[3]){
            return R.drawable.toowide;
        } else if (errorName == feedbackNames[4]){
            return R.drawable.bladeangle;
        }
        return R.drawable.perfect;
    }

    private String getExplination(String errorName){
        if (errorName == feedbackNames[1]){
            return "You are over reaching and leaning too far forward, try leaning back a bit and not hunching over.";
        } else if (errorName == feedbackNames[2]){
            return "You are leaning too far back in the seat, try sitting more upright and engaging your core";
        } else if (errorName == feedbackNames[3]){
            return "Your paddle isnt going into the water vertical enough, try holding your hands slightly further apart and really make sure the paddle is upright when going into the water";
        } else if (errorName == feedbackNames[4]){
            return "Your blade angle when taking stokes is wrong you are slicing through the water, try rotating the shaft a little but in your hands.";
        }
        return "";
    }
}
