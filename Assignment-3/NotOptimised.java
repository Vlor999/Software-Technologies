import java.util.ArrayList;
import java.util.List;

public class NotOptimised {

    public static void main(String[] args) {
        List<Integer> list = new ArrayList<Integer>();
        boolean everysecond = true;
        int loop = 250000;
        int counter = 0;

        for (int i = 0; i < loop; i++) {
            if (everysecond)
                everysecond = false;
            else
                everysecond = true;

            if (everysecond)
                list.add(i);
        }

        for (int i = 0; i < loop; i++) {
            if (everysecond)
                everysecond = false;
            else
                everysecond = true;

            if (everysecond) {
                if (list.contains(i)) {
                    System.out.println(list.get(counter));
                    counter++;
                }
            }
        }
    }
}
