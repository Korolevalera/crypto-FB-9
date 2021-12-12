import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Map;
import java.util.Scanner;
import java.util.stream.Collectors;

public class Main {
    public static void main(String[] args) throws IOException {
        Main main = new Main();
        System.out.println("Need filter ?");
        Scanner in = new Scanner(System.in);
        if (in.nextInt() == 1) {
            String rawText = Files.lines(Paths.get("text.txt")).collect(Collectors.joining());
            String filteredText = rawText.toLowerCase()
                    .chars()
                    .mapToObj(c -> (char) c)
                    .map(n -> {
                        if (n == 'ё') {
                            n = 'е';
                        } else if (n == 'ъ') {
                            n = 'ь';
                        }
                        return n;
                    }).filter(n -> n == ' ' || Character.UnicodeBlock.of(n).equals(Character.UnicodeBlock.CYRILLIC))
                    .map(String::valueOf).collect(Collectors.joining());
            try (PrintWriter out = new PrintWriter("output.txt", "UTF-8")) {
                out.write(filteredText.trim().replaceAll("\\s+", " "));
            }
            try (PrintWriter out = new PrintWriter("output_no_spaces.txt", "UTF-8")) {
                out.write(filteredText.trim().replaceAll("\\s+", ""));
            }
        }


        String text = Files.lines(Paths.get("output.txt")).collect(Collectors.joining());
        String textNoSpaces = Files.lines(Paths.get("output_no_spaces.txt")).collect(Collectors.joining());

        main.freqMono(text, true);
        main.freqMono(textNoSpaces, false);

        main.freqBiIntersection(text, true);
        main.freqBiIntersection(textNoSpaces, false);

        main.freqBiNoIntersection(text, true);
        main.freqBiNoIntersection(textNoSpaces, false);
    }

    void freqMono(String s, boolean b) {
        int n = 31;
        if (b) {
            n = 32;
            System.out.println("Mono frequency: ");
        } else {
            System.out.println("Mono no spaces frequency: ");

        }
        HashMap<Character, Integer> freqMono = new HashMap<>();
        s.chars()
                .mapToObj(c -> (char) c)
                .forEach(c -> {
                    if (freqMono.containsKey(c)) {
                        freqMono.put(c, freqMono.get(c) + 1);
                    } else {
                        freqMono.put(c, 1);
                    }
                });
        LinkedHashMap<Character, Integer> map = freqMono.entrySet().stream()
                .sorted((k1, k2) -> -k1.getValue().compareTo(k2.getValue())).collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue,
                (e1, e2) -> e1, LinkedHashMap::new));

        float entropy = 0;
        for (Map.Entry<Character, Integer> entry : map.entrySet()) {
            float freq = (float) entry.getValue() / s.length();
            System.out.println("'" + entry.getKey() + "'" + " " + freq);
            entropy += - freq * (Math.log(freq) / Math.log(2));
        }
        System.out.println("Entropy: " + entropy);
        System.out.println("Redundancy: " + (1 - (entropy / (Math.log(n) / Math.log(2)))));
    }

    void freqBiIntersection(String s, boolean b) {
        int n = 31;
        if (b) {
            n = 32;
            System.out.println("Bi frequency: ");
        } else {
            System.out.println("Bi no spaces frequency: ");
        }
        HashMap<String, Integer> freqBiIntersection = new HashMap<>();
        for (int i = 0; i < s.length() - 1; i++) {
            String bi = "" + s.charAt(i) + s.charAt(i+1);
            if (freqBiIntersection.containsKey(bi)) {
                freqBiIntersection.put(bi, freqBiIntersection.get(bi) + 1);
            } else {
                freqBiIntersection.put(bi, 1);
            }
        }
        LinkedHashMap<String, Integer> map = freqBiIntersection.entrySet().stream()
                .sorted((k1, k2) -> -k1.getValue().compareTo(k2.getValue())).collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue,
                        (e1, e2) -> e1, LinkedHashMap::new));

        float entropy = 0;
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            float freq = (float) entry.getValue() / (s.length() - 1);
            System.out.println("'" + entry.getKey() + "'" + " " + freq);
            entropy += - freq * (Math.log(freq) / Math.log(2));
        }
        entropy *= (float) 1 / 2;
        System.out.println("Entropy: " + entropy);
        System.out.println("Redundancy: " + (1 - (entropy / (Math.log(n) / Math.log(2)))));
    }

    void freqBiNoIntersection(String s, boolean b) {
        int n = 31;
        if (b) {
            n = 32;
            System.out.println("Bi no intersection frequency: ");
        } else {
            System.out.println("Bi no intersection no spaces frequency: ");
        }
        HashMap<String, Integer> freqBiNoIntersection = new HashMap<>();
        for (int i = 0; i < s.length() - 1; i+=2) {
            String bi = "" + s.charAt(i) + s.charAt(i+1);
            if (freqBiNoIntersection.containsKey(bi)) {
                freqBiNoIntersection.put(bi, freqBiNoIntersection.get(bi) + 1);
            } else {
                freqBiNoIntersection.put(bi, 1);
            }
        }

        LinkedHashMap<String, Integer> map = freqBiNoIntersection.entrySet().stream()
                .sorted((k1, k2) -> -k1.getValue().compareTo(k2.getValue())).collect(Collectors.toMap(Map.Entry::getKey, Map.Entry::getValue,
                        (e1, e2) -> e1, LinkedHashMap::new));

        float entropy = 0;
        for (Map.Entry<String, Integer> entry : map.entrySet()) {
            float freq = (float) entry.getValue() / ((float) s.length() / 2);
            System.out.println("'" + entry.getKey() + "'" + " " + freq);
            entropy += - freq * (Math.log(freq) / Math.log(2));
        }
        entropy *= (float) 1 / 2;
        System.out.println("Entropy: " + entropy);
        System.out.println("Redundancy: " + (1 - (entropy / (Math.log(n) / Math.log(2)))));
    }
}
