package com.adrian.sandoval.smartlockapp;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothManager;
import android.content.ActivityNotFoundException;
import android.content.Context;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.os.RemoteException;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
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

import java.text.DecimalFormat;
import java.util.Collection;

public class MainActivity extends AppCompatActivity implements BeaconConsumer, RangeNotifier {

    private static String TAG = "MyActivity";
    private BeaconManager mBeaconManager;

    //Bluetooth adapter
    private BluetoothAdapter bluetoothAdapter;

    //Request number must be greater than 0
    private final static int REQUEST_ENABLE_BT = 1;

    //button
    Button mbutton = null;

    TextView dis, mUrl, mresponse = null;

    String sending_url = null;

    RequestQueue queue = null;

    private static DecimalFormat decimalFormat = new DecimalFormat("0.00");

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        if (!getPackageManager().hasSystemFeature(PackageManager.FEATURE_BLUETOOTH_LE)) {
            Toast.makeText(this, "BLE NOT SUPPORTED", Toast.LENGTH_SHORT).show();
            finish();
        }

        // Bluetooth Manager
        final BluetoothManager bluetoothManager = (BluetoothManager) getSystemService(Context.BLUETOOTH_SERVICE);
        bluetoothAdapter = bluetoothManager.getAdapter();


        //Check to see if bluetooth is turned on, if not an Intent is called to allow to connect to BT
        if (bluetoothAdapter == null || !bluetoothAdapter.isEnabled())
        {
            try {
                Intent enableBtIntent = new Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE);
                startActivityForResult(enableBtIntent, REQUEST_ENABLE_BT);

            } catch (ActivityNotFoundException ex) {
                Log.d("ACTIVITY", ex.getMessage());
            }
        }


        mbutton = this.findViewById(R.id.login_btn);
        dis = this.findViewById(R.id.distance_id);
        mUrl = this.findViewById(R.id.url_id);
        mresponse = this.findViewById(R.id.response_id);

        mbutton.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
//                Intent intent = new Intent(v.getContext(), Home.class);
//                intent.setFlags(Intent.FLAG_ACTIVITY_REORDER_TO_FRONT);
//                v.getContext().startActivity(intent);
                login();
            }
        });

        queue = Volley.newRequestQueue(this);
//
//        BeaconManager beaconManager = BeaconManager.getInstanceForApplication(this.getApplicationContext());
//        // Detect the main identifier (UID) frame:
//        beaconManager.getBeaconParsers().add(new BeaconParser().setBeaconLayout(BeaconParser.EDDYSTONE_UID_LAYOUT));
//        // Detect the telemetry (TLM) frame:
//        beaconManager.getBeaconParsers().add(new BeaconParser().setBeaconLayout(BeaconParser.EDDYSTONE_TLM_LAYOUT));
//        // Detect the URL frame:
//        beaconManager.getBeaconParsers().add(new BeaconParser().setBeaconLayout(BeaconParser.EDDYSTONE_URL_LAYOUT));

    }



    public void login()
    {
        sending_url = sending_url + "5000/";

        StringRequest stringRequest = new StringRequest(Request.Method.POST, sending_url,
                new Response.Listener<String>() {
                    @Override
                    public void onResponse(String response) {
                        // Display the first 500 characters of the response string.
                        mresponse.setText("Response is: "+ response);
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                mresponse.setText("That didn't work!: " + error.toString());
                Log.d("Connection", error.toString());
            }
        });

        queue.add(stringRequest);

    }


    @Override
    public void onResume() {
        super.onResume();
        mBeaconManager = BeaconManager.getInstanceForApplication(this.getApplicationContext());
        // Detect the URL frame:
        mBeaconManager.getBeaconParsers().add(new BeaconParser().
                setBeaconLayout(BeaconParser.EDDYSTONE_URL_LAYOUT));
        mBeaconManager.bind(this);
    }


    public void onBeaconServiceConnect() {
        Region region = new Region("all-beacons-region", null, null, null);
        try {
            mBeaconManager.startRangingBeaconsInRegion(region);
        } catch (RemoteException e) {
            e.printStackTrace();
        }
        mBeaconManager.setRangeNotifier(this);
    }

    @Override
    public void didRangeBeaconsInRegion(Collection<Beacon> beacons, Region region) {
        for (Beacon beacon: beacons) {
            if (beacon.getServiceUuid() == 0xfeaa && beacon.getBeaconTypeCode() == 0x10) {
                // This is a Eddystone-URL frame
                String url = UrlBeaconUrlCompressor.uncompress(beacon.getId1().toByteArray());
                sending_url = url;
                Log.d(TAG, "I see a beacon transmitting a url: " + url +
                        " approximately " + beacon.getDistance() + " meters away.");
                dis.setText("Distance: " + decimalFormat.format(beacon.getDistance()));
                mUrl.setText("Advertising: " +url);


            }
        }
    }


    @Override
    public void onPause() {
        super.onPause();
        mBeaconManager.unbind(this);
    }




}
