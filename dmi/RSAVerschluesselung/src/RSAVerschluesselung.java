import java.math.BigInteger;

public class RSAVerschluesselung {
    public static void main(String[] args) {
        BigInteger zu_verschluesseln = new BigInteger("32");
        int schluessel = 5; // a oder b
        BigInteger n = new BigInteger("65");

        System.out.println((zu_verschluesseln.pow(schluessel)).mod(n));
    }
}
