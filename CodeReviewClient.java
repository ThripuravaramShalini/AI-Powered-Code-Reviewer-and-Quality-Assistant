import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.nio.file.Files;
import java.nio.file.Path;
import java.time.Duration;

public class CodeReviewClient {

    private static String escapeJson(String value) {
        return value.replace("\\", "\\\\")
                    .replace("\"", "\\\"")
                    .replace("\n", "\\n")
                    .replace("\r", "\\r")
                    .replace("\t", "\\t");
    }

    public static void main(String[] args) {
        if (args.length != 1) {
            System.out.println("Usage: java CodeReviewClient <source-file>");
            return;
        }

        Path file = Path.of(args[0]);
        if (!Files.exists(file)) {
            System.out.println("File not found: " + file);
            return;
        }

        String language = file.toString().toLowerCase().endsWith(".py")
                ? "python" : "java";

        try {
            String source = Files.readString(file);
            String body = "{\"language\":\"" + language
                    + "\",\"code\":\"" + escapeJson(source) + "\"}";

            HttpClient client = HttpClient.newBuilder()
                    .connectTimeout(Duration.ofSeconds(10)).build();

            HttpRequest request = HttpRequest.newBuilder()
                    .uri(URI.create("http://127.0.0.1:5000/review"))
                    .timeout(Duration.ofSeconds(30))
                    .header("Content-Type", "application/json")
                    .POST(HttpRequest.BodyPublishers.ofString(body))
                    .build();

            HttpResponse<String> response = client.send(
                    request, HttpResponse.BodyHandlers.ofString());

            System.out.println("HTTP Status: " + response.statusCode());
            System.out.println("Code Review Result:");
            System.out.println(response.body());

        } catch (InterruptedException ex) {
            Thread.currentThread().interrupt();
            System.out.println("Request interrupted.");
        } catch (Exception ex) {
            System.out.println("Error: " + ex.getMessage());
            System.out.println("Check that the Python API is running on port 5000.");
        }
    }
}
