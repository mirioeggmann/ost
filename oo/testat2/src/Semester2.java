import java.util.HashSet;
import java.util.Set;

public class Semester2 {
    private final int number;
    private final Set<Module2> modules = new HashSet<>();

    public Semester2(int number) {
        this.number = number;
    }

    public int getNumber() {
        return number;
    }

    public Set<Module2> getModules() {
        return modules;
    }
}
