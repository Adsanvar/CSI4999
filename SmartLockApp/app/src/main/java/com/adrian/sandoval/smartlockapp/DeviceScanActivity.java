package com.adrian.sandoval.smartlockapp;

import android.Manifest;
import android.bluetooth.BluetoothAdapter;
import android.bluetooth.BluetoothDevice;
import android.bluetooth.le.BluetoothLeScanner;
import android.bluetooth.le.ScanCallback;
import android.bluetooth.le.ScanResult;
import android.content.pm.PackageManager;
import android.os.Handler;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;

public class DeviceScanActivity extends AppCompatActivity {

    private BluetoothAdapter bluetoothAdapter;
    private BluetoothLeScanner bluetoothLeScanner;
    private boolean mScanning;
    private Handler handler;
    private Button mStartScanBtn;

    // Stops scanning after 10 seconds.
    private static final long SCAN_PERIOD = 10000;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_device_scan);

        mStartScanBtn = (Button) findViewById(R.id.scan_le_btn);
        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter();
        bluetoothLeScanner = BluetoothAdapter.getDefaultAdapter().getBluetoothLeScanner();
        handler = new Handler();

        ActivityCompat.requestPermissions(this,new String[]{Manifest.permission.ACCESS_FINE_LOCATION, Manifest.permission.ACCESS_COARSE_LOCATION}, 1001);

        mStartScanBtn.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(mScanning)
                {
                    mScanning = false;
                    scanLeDevice(false);
                    mStartScanBtn.setText("Stop");
                }
                else
                {
                    mScanning = true;
                    scanLeDevice(true);
                    mStartScanBtn.setText("SCAN");
                }
            }
        });

    }


    private ScanCallback leScanCallBack  = new ScanCallback() {
        @Override
        public void onScanResult(int callbackType, ScanResult result) {
            //super.onScanResult(callbackType, result);
//            Log.d("Scanned", result.getDevice().toString());
            Log.d("Scanned", result.getDevice().getName() + " Address: " + result.getDevice().getAddress() + " | RSSI: " + Integer.toString(result.getRssi()));


        }

        @Override
        public void onScanFailed(int errorCode){
            super.onScanFailed(errorCode);
            Log.d("BLE", "Some Error: " + Integer.toString(errorCode));
        }
    };

    private void scanLeDevice(final boolean enable) {
        if (enable) {
            // Stops scanning after a pre-defined scan period.
            handler.postDelayed(new Runnable() {
                @Override
                public void run() {
                    Log.d("Scanning", "Start");
                    mScanning = false;
                    bluetoothLeScanner.startScan(leScanCallBack);
                }
            }, SCAN_PERIOD);


            Log.d("Scanning", "Initialized");
            mScanning = true;
            bluetoothLeScanner.startScan(leScanCallBack);
        } else {
            Log.d("Scanning", "Stopped");
            mScanning = false;
            bluetoothLeScanner.stopScan(leScanCallBack);
        }
    }

}
