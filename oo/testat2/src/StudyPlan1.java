import java.io.IOException;
import java.util.*;

public class StudyPlan1 {
    private final Map<String, Module1> modules;
    private Map<Integer, Semester1> semesters;
    private final String fileName;

    public StudyPlan1(String fileName) {
        modules = new HashMap<>();
        semesters = new HashMap<>();
        this.fileName = fileName;
    }

    public void initModules() throws IOException {
        try (var reader = new CatalogueReader1(fileName)) {
            String[] names;
            while ((names = reader.readNextLine()) != null) {
                if (!modules.containsKey(names[0])) {
                    modules.put(names[0], new Module1(names[0]));
                }
                var requiredModules = new HashSet<>(Arrays.asList(names).subList(1, names.length));
                for (String requiredModule : requiredModules) {
                    if (!modules.containsKey(requiredModule)) {
                        modules.put(requiredModule, new Module1(requiredModule));
                    }
                    modules.get(names[0]).addRequiredModule(modules.get(requiredModule));
                }
            }
        }
    }

    public void calculateStudyPlan() throws CycleDependencyException1 {
        var openModules = modules;
        semesters = new HashMap<>();

        int currentSemester = 1;
        while (openModules.size() > 0) {
            Semester1 semester = new Semester1(currentSemester);
            semester.getModules().addAll(getModulesWithoutDependencies(openModules));
            semesters.put(currentSemester, semester);
            for (Module1 module : openModules.values()) {
                module.getRequiredModules().removeAll(semesters.get(currentSemester).getModules());
            }
            openModules.values().removeAll(semesters.get(currentSemester).getModules());
            currentSemester++;
        }
    }

    public void printStudyPlan() {
        if (semesters.size() == 0) {
            System.out.println("Please make sure that you have a valid study cataloge before printing the study plan!");
        } else {
            for (Semester1 semester : semesters.values()) {
                System.out.print("Semester " + semester.getNumber() + ":");
                for (Module1 module : semester.getModules()) {
                    System.out.print(" " + module.getName());
                }
                System.out.println();
            }
        }
    }

    private Set<Module1> getModulesWithoutDependencies(Map<String, Module1> openModules) throws CycleDependencyException1 {
        var modulesWithoutDependencies = new HashSet<Module1>();
        for (Module1 module : openModules.values()) {
            if (module.getRequiredModules().isEmpty()) {
                modulesWithoutDependencies.add(module);
            }
        }
        if (modulesWithoutDependencies.isEmpty()) {
            throw new CycleDependencyException1("Cycle detected!");
        }
        return modulesWithoutDependencies;
    }
}
