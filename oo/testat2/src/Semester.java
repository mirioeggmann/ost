import java.util.HashSet;
import java.util.Set;

public class Semester {
    private final int number;
    private final Set<Module> modules = new HashSet<>();

    public Semester(int number) {
        this.number = number;
    }

    public int getNumber() {
        return number;
    }

    public Set<Module> getModules() {
        return modules;
    }
}
