import java.io.IOException;

public class Test1 {
    public static void main(String[] args) {
        var studyPlan = new StudyPlan1("LargeCatalogue.txt");
        try {
            studyPlan.initModules();
        } catch (IOException e) {
            System.out.println("Could not read the StudyCatalogue.txt from the file system!");
        }
        try {
            long start = System.currentTimeMillis();
            studyPlan.calculateStudyPlan();
            System.out.println("calculating the study plan took: " + (System.currentTimeMillis() - start) + "ms");
            studyPlan.printStudyPlan();
        } catch (CycleDependencyException e) {
            System.out.println("No calculations possible: " + e.getMessage());
        }
    }
}
