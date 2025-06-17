import java.util.*;
import java.math.*;

public class NonOpti {

    public static void main(String[] args) {
        
        //Exemple of a data set
        ArrayList<Double> list = new ArrayList<Double>();

        for (double i =0; i< 100000; i++){
            list.add(i);
        }

        
        for (int j=0;j<1000;j++){
            //Calculations on the data set list 
            System.out.println(sumPower(list,1));
            System.out.println(sumPower(list, 2));
            System.out.println(sumPower(list, 3));
            System.out.println(sumPower(list, 4));
            System.out.println(sumPower(list, 5));
        }
            
    }

    // @Param : set of values s, power p
    // @Return : sum(i^p for i in s)/length(s)^p
    private static Double sumPower(ArrayList<Double> s, int p){
        double sum = 0;
        for (double value : s) {
            sum += Math.pow(value, p);
        }
        return sum/Math.pow(s.size(),p);
    }
}
