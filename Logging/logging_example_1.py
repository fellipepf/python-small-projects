import logging
import math

#create and configure logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"

logging.basicConfig(filename="example_1.log",
                    level= logging.DEBUG,
                    format= LOG_FORMAT
                    )

logger = logging.getLogger()

def quadratic_formula(a,b,c):
    """
    :param a:
    :param b:
    :param c:
    :return: solutions to the equation ax^2 + bx + c = 0
    """
    logger.info("quadratic_formula({0}, {1}, {2})".format(a,b,c))

    #discriminant
    logger.debug("# Compute the discriminant")
    disc = b**2 -4*a*c

    #compute the roots
    logger.debug("# compute the two roots")
    try:
        root1 = (-b + math.sqrt(disc)) / (2*a)
        root2 = (-b - math.sqrt(disc)) / (2*a)

        #returm the roots
        logger.debug("# return the roots")
        return (root1, root2)

    except ValueError:
        logger.error("# error computing the roots")

roots = quadratic_formula(1,0, 1)
print(roots)


