package com.adrian.sandoval.smartlockapp;

import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.BluetoothGatt;
import android.bluetooth.BluetoothGattCallback;
import android.bluetooth.BluetoothGattCharacteristic;
import android.bluetooth.BluetoothGattDescriptor;
import android.content.Context;
import android.content.Intent;
import android.os.AsyncTask;
import android.os.Handler;
import android.os.RemoteException;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.view.animation.Animation;
import android.view.animation.AnimationUtils;
import android.widget.Button;
import android.widget.EditText;
import android.widget.ImageView;
import android.widget.Toast;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.altbeacon.beacon.Beacon;
import org.altbeacon.beacon.BeaconConsumer;
import org.altbeacon.beacon.BeaconManager;
import org.altbeacon.beacon.BeaconParser;
import org.altbeacon.beacon.RangeNotifier;
import org.altbeacon.beacon.Region;
import org.altbeacon.beacon.utils.UrlBeaconUrlCompressor;

import java.util.Collection;

public class Home extends AppCompatActivity {

private Button btnLogin;
private EditText txtUsername, txtPassword;
private ImageView logo;
private Context context;
private RequestQueue queue = null;
private Handler handler =null;
private Integer WAIT_PERIOD = null;
private String sending_url = null;
private Boolean authenticated = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        btnLogin = findViewById(R.id.btnLogin);
        txtUsername = findViewById(R.id.txtUsername);
        txtPassword = findViewById(R.id.txtPassword);
        logo = findViewById(R.id.logo);
        context = this;
        authenticated = false;

        sending_url = "http://192.168.1.65:5000/";


        Animation anim = AnimationUtils.loadAnimation(this, R.anim.fadein);
        logo.startAnimation(anim);
        txtUsername.startAnimation(anim);
        txtPassword.startAnimation(anim);
        btnLogin.startAnimation(anim);
        txtUsername.requestFocus();

        queue = Volley.newRequestQueue(this);
        handler = new Handler();
        WAIT_PERIOD = 1500;

        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                login(txtUsername.getText().toString(), txtPassword.getText().toString());

            }
        });

    }


//
//    final Animation animation = AnimationUtils.loadAnimation(context, R.anim.blink_anim);
//                Log.d("Authenticate", authenticated.toString());
//                if(authenticated)
//    {
//        Intent intent = new Intent(context, MainActivity.class);
//        context.startActivity(intent);
//        overridePendingTransition(R.anim.fadein, R.anim.fadeout);
//
//    }else{
//
//        Toast.makeText(context, "Invalid Credential", Toast.LENGTH_LONG).show();
//        btnLogin.setText("Error");
//        btnLogin.setTextColor(getResources().getColor(R.color.white));
//        btnLogin.startAnimation(animation);
//        btnLogin.setBackground(getResources().getDrawable(R.drawable.login_failed_button));
//
//    }
//
//                handler.postDelayed(new Runnable() {
//        @Override
//        public void run() {
//
//            btnLogin.setBackground(getResources().getDrawable(R.drawable.login_button));
//            btnLogin.setText("Login");
//            btnLogin.setTextColor(getResources().getColor(R.color.white));
//            btnLogin.clearAnimation();
//            animation.cancel();
//
//        }
//    }, WAIT_PERIOD);


    public void login(String usrname, String pas)
    {
        String req = sending_url + "mobilelogin/"+usrname+"/"+pas;

        new Home.SendRequest().execute(req);

    }

    protected class SendRequest extends AsyncTask<String, Integer, String> {
        String resp = null;

        protected  String doInBackground(final String... urls)
        {

            for(int i =0; i < urls.length; i++)
            {
                StringRequest stringRequest = new StringRequest(Request.Method.GET, urls[i],
                        new Response.Listener<String>() {
                            @Override
                            public void onResponse(String response) {
                                // Display the first 500 characters of the response string.
                                //mresponse.setText("Response is: "+ response);
                                if(response.equals("Success"))
                                {
                                    authenticated = true;
                                    Log.d("CONNECTION", authenticated.toString());

                                    Intent intent = new Intent(context, MainActivity.class);
                                    context.startActivity(intent);

                                }else{ authenticated = false; }

                                //Toast.makeText(context, "Response: " + resp.toString(), Toast.LENGTH_SHORT).show();
                            }
                        }, new Response.ErrorListener() {
                    @Override
                    public void onErrorResponse(VolleyError error) {
                        //mresponse.setText("That didn't work!: " + error.toString());
                        Log.d("Connection", error.toString());
                    }
                });

                queue.add(stringRequest);
            }

            return resp;

        }


        //When post has executed
//        @Override
//        protected  void onPostExecute(final String resp)
//        {

//
//            handler.postDelayed(new Runnable() {
//                @Override
//                public void run() {
//
//                    final Animation animation = AnimationUtils.loadAnimation(context, R.anim.blink_anim);
//                    Log.d("Authenticate", authenticated.toString());
//                    if(authenticated)
//                    {
//                        Intent intent = new Intent(context, MainActivity.class);
//                        context.startActivity(intent);
//                        overridePendingTransition(R.anim.fadein, R.anim.fadeout);
//
//                    }else{
//
//                        Toast.makeText(context, "Invalid Credential", Toast.LENGTH_LONG).show();
//                        btnLogin.setText("Error");
//                        btnLogin.setTextColor(getResources().getColor(R.color.white));
//                        btnLogin.startAnimation(animation);
//                        btnLogin.setBackground(getResources().getDrawable(R.drawable.login_failed_button));
//
//                    }
//
////                btnLogin.setBackground(getResources().getDrawable(R.drawable.login_button));
////                btnLogin.setText("Login");
////                btnLogin.setTextColor(getResources().getColor(R.color.white));
////                btnLogin.clearAnimation();
////                animation.cancel();
//
//                }
//            }, WAIT_PERIOD);




        //}
    }


}

