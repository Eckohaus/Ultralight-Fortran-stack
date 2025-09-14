program ultralight
    implicit none
    real :: m, c, E

    ! Read mass from command-line argument
    call getarg(1, m)

    ! Speed of light
    c = 299792458.0

    ! Equation: E = mc^2
    E = m * c**2

    print *, E
end program ultralight

