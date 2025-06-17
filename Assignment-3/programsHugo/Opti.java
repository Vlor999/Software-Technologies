import java.util.*;
import java.math.*;

public class Opti {

    public static void main(String[] args) {
        
        //Exemple of a data set
        ArrayList<Double> list = new ArrayList<Double>();

        for (double i =0; i< 100000; i++){
            list.add(i);
        }

        
        //Calculations on the data set list 
        for (int j=0;j<1000;j++){
            sumPower(list);
        }
         
    }


    // Param : set of values s, power p
    // Return : sum(i^p for i in s)/length(s)^p for p=1,2,3
    private static void sumPower(ArrayList<Double> s){

        double sum1 = 0;
        double sum2 = 0;
        double sum3 = 0;
        double sum4 = 0;
        double sum5 = 0;
        
        for (double value : s) {
            sum1 += value;
            sum2 += Math.pow(value,2);
            sum3 += Math.pow(value,3);
            sum4 += Math.pow(value,4);
            sum5 += Math.pow(value,5);

        }
        int length = s.size();
        System.out.println(sum1/length);
        System.out.println(sum2/Math.pow(length,2));
        System.out.println(sum3/Math.pow(length,3));
        System.out.println(sum4/Math.pow(length,4));
        System.out.println(sum5/Math.pow(length,5));
    }
}
