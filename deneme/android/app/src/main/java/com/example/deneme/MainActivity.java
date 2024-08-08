package com.example.deneme;

import android.content.res.AssetManager;
import android.os.Bundle;
import android.os.FileUtils;
import androidx.annotation.NonNull;
import io.flutter.embedding.android.FlutterActivity;
import io.flutter.embedding.engine.FlutterEngine;
import io.flutter.plugin.common.MethodCall;
import io.flutter.plugin.common.MethodChannel;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;

public class MainActivity extends FlutterActivity {
    private static final String CHANNEL = "plaka_tanima_channel";

    @Override
    public void configureFlutterEngine(@NonNull FlutterEngine flutterEngine) {
        super.configureFlutterEngine(flutterEngine);

        new MethodChannel(flutterEngine.getDartExecutor().getBinaryMessenger(), CHANNEL)
                .setMethodCallHandler(
                        (call, result) -> {
                            if (call.method.equals("runBinary")) {
                                String output = runBinary();
                                if (output != null) {
                                    result.success(output);
                                } else {
                                    result.error("UNAVAILABLE", "Binary run failed", null);
                                }
                            } else {
                                result.notImplemented();
                            }
                        }
                );
    }

    private String runBinary() {
        try {
            // Copy binary from assets to a file in internal storage
            AssetManager assetManager = getAssets();
            File binaryFile = new File(getFilesDir(), "detector");
            try (InputStream in = assetManager.open("detector");
                 OutputStream out = new FileOutputStream(binaryFile)) {
                byte[] buffer = new byte[1024];
                int read;
                while ((read = in.read(buffer)) != -1) {
                    out.write(buffer, 0, read);
                }
            }

            // Make the file executable
            binaryFile.setExecutable(true);

            // Execute the binary file
            Process process = Runtime.getRuntime().exec(binaryFile.getAbsolutePath());
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            process.waitFor();
            return output.toString();
        } catch (IOException | InterruptedException e) {
            e.printStackTrace();
            return null;
        }
    }
}
