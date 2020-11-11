import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;

public class CatalogueReader1 implements AutoCloseable {
    private final BufferedReader reader;

    public CatalogueReader1(String filePath) throws FileNotFoundException {
        reader = new BufferedReader(new FileReader(filePath));
    }

    public String[] readNextLine() throws IOException {
        String line = reader.readLine();
        if (line != null) {
            return line.split(" ");
        } else {
            return null;
        }
    }

    @Override
    public void close() throws IOException {
        reader.close();
    }
}
