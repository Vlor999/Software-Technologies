package programsWillem;

import java.util.concurrent.*;

public class HeavyFibonacci {


    public double expo_fibo(double val, int n) {
        if (n == 0) {
            return 1.0;
        }
        double noise = 0.0;
        for (int i = 1; i <= 10000; i++) {
            noise += Math.sin(val) * Math.sqrt(i);
        }
        return val * expo_fibo(val, n - 1) + noise * 1e-10;
    }

    public double run(int endValue, int puissance) {
        if (endValue <= 0) return 0;
        if (endValue == 1) return 0;
        if (endValue == 2) return 1;

        double[] memory = new double[endValue];
        memory[0] = 0;
        memory[1] = 1;
        for (int i = 2; i < endValue; i++) {
            memory[i] = expo_fibo(this.run(i-1, 1), puissance) + expo_fibo(this.run(i-2, 1), puissance);
        }
        return memory[endValue - 1];
    }

    public static void main(String[] args) throws InterruptedException {
        final int n = 30;
        final int puissance = 25;
        final HeavyFibonacci fib = new HeavyFibonacci();

        ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());

        System.out.println("Démarrage du calcul lourd...");
        long start = System.currentTimeMillis();

        for (int i = 10; i < n; i++) {
            final int index = i;
            executor.submit(() -> {
                double res = fib.run(index, puissance);
                System.out.println("Résultat pour n=" + index + ": " + res);
            });
        }

        executor.shutdown();
        executor.awaitTermination(1, TimeUnit.HOURS);

        long end = System.currentTimeMillis();
        System.out.println("Temps total (ms) : " + (end - start));
    }
}
