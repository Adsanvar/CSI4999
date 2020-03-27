package com.adrian.sandoval.smartlockapp;

import android.app.Activity;
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
private RequestQueue queue = null;
private Handler handler =null;
private Integer WAIT_PERIOD = null;
private String sending_url = null;
private Boolean authenticated = null;
private Animation animation_1, animation_2 = null;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        btnLogin = findViewById(R.id.btnLogin);
        txtUsername = findViewById(R.id.txtUsername);
        txtPassword = findViewById(R.id.txtPassword);
        logo = findViewById(R.id.logo);
        authenticated = false;

        //sending_url = "http://adsanvar.pythonanywhere.com/";
        sending_url = "http://192.168.1.74:5000/";


        Animation anim = AnimationUtils.loadAnimation(this, R.anim.fadein);
        logo.startAnimation(anim);
        txtUsername.startAnimation(anim);
        txtPassword.startAnimation(anim);
        btnLogin.startAnimation(anim);
        txtUsername.requestFocus();

        queue = Volley.newRequestQueue(this);
        handler = new Handler();
        WAIT_PERIOD = 1500;

        animation_1 = AnimationUtils.loadAnimation(this, R.anim.rotate);


        btnLogin.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {

                login(txtUsername.getText().toString(), txtPassword.getText().toString(), v.getContext());

                btnLogin.startAnimation(animation_1);


            }
        });

    }


    public void login(String usrname, String pas, final Context context) {
        final String req = sending_url + "mobilelogin/" + usrname + "/" + pas;
        final String info = sending_url + "getUserInfo/"+usrname;
        animation_2 = AnimationUtils.loadAnimation(context, R.anim.blink_anim);

        //new Home.SendRequest().execute(req);

        StringRequest stringRequest = new StringRequest(Request.Method.GET, req,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 500 characters of the response string.
                        //mresponse.setText("Response is: "+ response);
                        if (response.equals("Success")) {
                            btnLogin.clearAnimation();
                            animation_1.cancel();
                            btnLogin.clearAnimation();
                            animation_2.cancel();
                            authenticated = true;
                            getUserInformation(context, info);
                        }

                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                //mresponse.setText("That didn't work!: " + error.toString());
                Log.d("Connection", error.toString());

                    animation_1.cancel();
                    btnLogin.clearAnimation();
                    Toast.makeText(context, "Invalid Credential", Toast.LENGTH_LONG).show();
                    btnLogin.setText("Error");
                    btnLogin.setTextColor(getResources().getColor(R.color.white));
                    btnLogin.startAnimation(animation_2);
                    btnLogin.setBackground(getResources().getDrawable(R.drawable.login_failed_button));
                    authenticated = false;

                handler.postDelayed(new Runnable() {
                    @Override
                    public void run() {

                        btnLogin.setBackground(getResources().getDrawable(R.drawable.login_button));
                        btnLogin.setText("Login");
                        btnLogin.setTextColor(getResources().getColor(R.color.white));
                        btnLogin.clearAnimation();
                        animation_2.cancel();

                    }
                }, WAIT_PERIOD);
            }
        });

        queue.add(stringRequest);
    }


    protected void getUserInformation(Context context, String req)
    {
        final Context context1 = context;
        StringRequest stringRequest1 = new StringRequest(Request.Method.GET, req, new Response.Listener<String>() {
            @Override
            public void onResponse(String response) {
                Toast.makeText(context1, "inGetUserInfo", Toast.LENGTH_LONG).show();
                Intent intent = new Intent(context1, MainActivity.class);
                intent.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
                context1.startActivity(intent);

            }
        }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                Toast.makeText(context1, "Unable To Acquire User Info", Toast.LENGTH_LONG).show();
            }
        });

        queue.add(stringRequest1);

    }

}

