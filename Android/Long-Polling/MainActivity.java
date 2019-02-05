package com.example.shashankavs.npiot;

import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.os.AsyncTask;
import android.os.StrictMode;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.ImageView;
import android.widget.TextView;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.net.MalformedURLException;
import java.net.URL;

public class MainActivity extends AppCompatActivity {

    static TextView textView2;
    private static final String TAG = "MainActivity";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (android.os.Build.VERSION.SDK_INT > 9) {
            StrictMode.ThreadPolicy policy = new StrictMode.ThreadPolicy.Builder().permitAll().build();
            StrictMode.setThreadPolicy(policy);
        }

        TextView tv = (TextView) findViewById(R.id.textView2);
        try {
            // Create a URL for the desired page
            URL url = new URL("http://52.207.185.193:8000/details.txt");

            // Read all the text returned by the server
            BufferedReader in = new BufferedReader(new InputStreamReader(url.openStream()));
            String str;
            StringBuilder sb = new StringBuilder(100);
            while ((str = in.readLine()) != null) {
                sb.append(str);
                // str is one line of text; readLine() strips the newline character(s)
            }
            in.close();
            tv.setText(sb.toString());
        } catch (MalformedURLException e) {
            tv.setText("mal");
        } catch (IOException e) {
            tv.setText("io");
        }

        for(int j = 0; j <= 1000; j++) {
            for (int i = 0; i < 29; i++) {
                String index = String.valueOf(i);
                String url = "http://52.207.185.193:8000/image" + index + ".jpg";
                new DownloadImageFromInternet((ImageView) findViewById(R.id.imageView))
                        .execute(url);
            }
        }
    }

    public void yesMessage(View view) {
        Intent yesintent = new Intent(this, YesActivity.class);
        startActivity(yesintent);
    }

    private class DownloadImageFromInternet extends AsyncTask<String, Void, Bitmap> {
        ImageView imageView;

        public DownloadImageFromInternet(ImageView imageView) {
            this.imageView = imageView;
        }

        protected Bitmap doInBackground(String... urls) {
            String imageURL = urls[0];
            Bitmap bimage = null;
            try {
                InputStream in = new java.net.URL(imageURL).openStream();
                bimage = BitmapFactory.decodeStream(in);

            } catch (Exception e) {
                Log.e("Error Message", e.getMessage());
                e.printStackTrace();
            }
            return bimage;
        }

        protected void onPostExecute(Bitmap result) {
            imageView.setImageBitmap(result);
        }
    }
}
