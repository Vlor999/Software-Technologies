import java.util.ArrayList;
import java.util.List;

public class Optimised {
    public static void main(String[] args) {
        int loop = 250000;
        Integer[] array = new Integer[loop/2 + loop%2];
        int counter = 0;

        for (int i = 0; i < loop; i = i + 2) {
            array[counter] = i;
            counter++;
        }

        counter = 0;
        for (int i = 0; i < loop; i = i + 2) {
            System.out.println(array[counter]);
            counter++;
        }
    }
}
