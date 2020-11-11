import java.util.HashSet;
import java.util.Set;

public class Semester1 {
    private final int number;
    private final Set<Module1> modules = new HashSet<>();

    public Semester1(int number) {
        this.number = number;
    }

    public int getNumber() {
        return number;
    }

    public Set<Module1> getModules() {
        return modules;
    }
}
