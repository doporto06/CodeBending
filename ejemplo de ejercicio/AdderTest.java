import org.junit.jupiter.api.Test;
import static org.junit.jupiter.api.Assertions.assertEquals;

public class AdderTest {
    @Test
    void testAddTwoWith1And2() {
        assertEquals(3, Adder.addTwo(1, 2));
    }

    @Test
    void testAddTwoWith5And4() {
        assertEquals(9, Adder.addTwo(5, 4));
    }
}