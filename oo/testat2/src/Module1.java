import java.util.HashSet;
import java.util.Objects;
import java.util.Set;

public class Module1 {
    private final String name;
    private final Set<Module1> requiredModules = new HashSet<>();

    public Module1(String name) {
        this.name = name;
    }

    public void addRequiredModule(Module1 module) {
        requiredModules.add(module);
    }

    public String getName() {
        return name;
    }

    public Set<Module1> getRequiredModules() {
        return requiredModules;
    }

    @Override
    public String toString() {
        return "Module{" +
                "name='" + name + '\'' +
                ", requiredModules=" + requiredModules +
                '}';
    }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (o == null || getClass() != o.getClass()) return false;
        Module1 module = (Module1) o;
        return Objects.equals(name, module.name);
    }

    @Override
    public int hashCode() {
        return Objects.hash(name);
    }
}
