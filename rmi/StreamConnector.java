import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.io.OutputStreamWriter;

class StreamConnector extends Thread
{
  InputStream hx;
  OutputStream il;

  StreamConnector(InputStream hx, OutputStream il)
  {
    this.hx = hx;
    this.il = il;
  }

  public void run() {
    BufferedReader ar = null;
    BufferedWriter slm = null;
    try {
      ar = new BufferedReader(new InputStreamReader(this.hx));
      slm = new BufferedWriter(new OutputStreamWriter(this.il));
      char[] buffer = new char[8192];
      int length;
      while ((length = ar.read(buffer, 0, buffer.length)) > 0)
      {
        slm.write(buffer, 0, length);
        slm.flush();
      }
    } catch (Exception localException) {
    }
    try {
      if (ar != null)
        ar.close();
      if (slm != null)
        slm.close();
    }
    catch (Exception localException1)
    {
    }
  }
}