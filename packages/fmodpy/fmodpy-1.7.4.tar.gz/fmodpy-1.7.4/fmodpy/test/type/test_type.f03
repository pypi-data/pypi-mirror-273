MODULE FTYPES
  TYPE, BIND(C) :: SIZE_TYPE
     INTEGER :: N
  END TYPE SIZE_TYPE

  TYPE, BIND(C) :: T1
     INTEGER :: A
     REAL :: B
  END TYPE T1

  TYPE, BIND(C) :: T2
     INTEGER :: A
     REAL :: B
  END TYPE T2

CONTAINS

  SUBROUTINE COPY_T1_TO_T2(A, B)
    TYPE(T1), INTENT(IN) :: A
    TYPE(T2), INTENT(OUT) :: B
    B%A = A%A
    B%B = A%B
  END SUBROUTINE COPY_T1_TO_T2

END MODULE FTYPES

! Test Fortran REAL wrapping and usage from Python with fmodpy.

SUBROUTINE TEST_STANDARD(SING_IN, SING_OUT, ARRAY_IN, ARRAY_OUT,&
     KNOWN_ARRAY_OUT, KNOWN_MATRIX_OUT, OPT_SING_IN, OPT_SING_OUT)
  ! Test the basic functionaly of the 'TYPE(T1)' type and its
  ! interoperability with Python. This includes, inputs, outputs,
  ! array inputs with known and unknown size, optional inputs, and
  ! optional outputs. 
  IMPLICIT NONE
  TYPE, BIND(C) :: T2
     INTEGER :: A
     REAL :: B
  END TYPE T2
  ! Argument definitions.
  TYPE(T2), INTENT(IN) :: SING_IN
  TYPE(T2), INTENT(OUT) :: SING_OUT
  TYPE(T2), DIMENSION(:), INTENT(IN) :: ARRAY_IN
  TYPE(T2), DIMENSION(:), INTENT(OUT) :: ARRAY_OUT
  TYPE(T2), DIMENSION(SIZE(ARRAY_OUT)), INTENT(OUT) :: KNOWN_ARRAY_OUT
  TYPE(T2), DIMENSION(3,SIZE(ARRAY_OUT)), INTENT(OUT) :: KNOWN_MATRIX_OUT
  TYPE(T2), INTENT(IN), OPTIONAL :: OPT_SING_IN
  TYPE(T2), INTENT(OUT), OPTIONAL :: OPT_SING_OUT
  ! Local variable.
  INTEGER :: I
  ! Copy the single input value to the single output value.
  SING_OUT%A = SING_IN%A + 1
  SING_OUT%B = SING_IN%B + 1.0
  ! Copy as much of the input array as possible to the output array.
  ARRAY_OUT(1:MIN(SIZE(ARRAY_IN),SIZE(ARRAY_OUT))) = &
       &ARRAY_IN(1:MIN(SIZE(ARRAY_IN),SIZE(ARRAY_OUT)))
  DO I = MIN(SIZE(ARRAY_IN),SIZE(ARRAY_OUT))+1, SIZE(ARRAY_OUT)
     ARRAY_OUT(I)%A = I
     ARRAY_OUT(I)%B = REAL(I)
  END DO
  DO I = 1, SIZE(KNOWN_MATRIX_OUT, 1)
     KNOWN_MATRIX_OUT(I,:)%A = I
     KNOWN_MATRIX_OUT(I,:)%B = REAL(I)
  END DO
  ! Set the KNOWN_ARRAY and the KNOWN_MATRIX values to be identifiabl.
  DO I = 1,SIZE(ARRAY_OUT)
     KNOWN_ARRAY_OUT(I)%A = I
     KNOWN_ARRAY_OUT(I)%B = REAL(I)
     KNOWN_MATRIX_OUT(:,I)%A = KNOWN_MATRIX_OUT(:,I)%A + I
     KNOWN_MATRIX_OUT(:,I)%B = KNOWN_MATRIX_OUT(:,I)%B + REAL(I)
  END DO
  ! Do some operations on the optional inputs / outputs.
  IF (PRESENT(OPT_SING_OUT)) THEN
     IF (PRESENT(OPT_SING_IN)) THEN
        OPT_SING_OUT = OPT_SING_IN
     ELSE
        OPT_SING_OUT = SING_IN
     END IF
  ELSE IF (PRESENT(OPT_SING_IN)) THEN
     SING_OUT = OPT_SING_IN
  END IF
  ! End of this subroutine.
END SUBROUTINE TEST_STANDARD


FUNCTION TEST_EXTENDED(OPT_ARRAY_IN, KNOWN_OPT_ARRAY_OUT,&
     & OPT_ALLOC_ARRAY_OUT, N ) RESULT(ALLOC_ARRAY_OUT)
  ! Test the extended functionaly of the 'TYPE(T1)' type and its
  ! interoperability with Python. This includes, optional array
  ! inputs, optional array outputs, and allocatable array outputs.
  USE FTYPES, ONLY: T1
  IMPLICIT NONE
  TYPE(T1), INTENT(IN), OPTIONAL, DIMENSION(:) :: OPT_ARRAY_IN
  TYPE(T1), INTENT(OUT), OPTIONAL :: KNOWN_OPT_ARRAY_OUT(3)
  TYPE(T1), INTENT(OUT), OPTIONAL, ALLOCATABLE :: OPT_ALLOC_ARRAY_OUT(:)
  TYPE(T1), DIMENSION(:), ALLOCATABLE :: ALLOC_ARRAY_OUT
  INTEGER, INTENT(IN) :: N
  ! Local variable.
  INTEGER :: I

  ! Assign the optional array output values.
  IF (PRESENT(KNOWN_OPT_ARRAY_OUT)) THEN
     IF (PRESENT(OPT_ARRAY_IN)) THEN
        DO I = 1, MIN(SIZE(OPT_ARRAY_IN), SIZE(KNOWN_OPT_ARRAY_OUT))
           KNOWN_OPT_ARRAY_OUT(I)%A = I
           KNOWN_OPT_ARRAY_OUT(I)%B = REAL(I)
        END DO
     ELSE
        DO I = 1, SIZE(KNOWN_OPT_ARRAY_OUT)
           KNOWN_OPT_ARRAY_OUT(I)%A = I
           KNOWN_OPT_ARRAY_OUT(I)%B = REAL(I)
        END DO
     END IF

  END IF

  ! Allocate the optional array output and assign its values.
  IF (PRESENT(OPT_ALLOC_ARRAY_OUT)) THEN
     ALLOCATE(OPT_ALLOC_ARRAY_OUT(1:N/2))
     DO I = 1, SIZE(OPT_ALLOC_ARRAY_OUT)
        OPT_ALLOC_ARRAY_OUT(I)%A = SIZE(OPT_ALLOC_ARRAY_OUT) - (I-1)
        OPT_ALLOC_ARRAY_OUT(I)%B = REAL(SIZE(OPT_ALLOC_ARRAY_OUT) - (I-1))
     END DO

  END IF
  
  ! Allocate the required array output to the specified size.
  ALLOCATE(ALLOC_ARRAY_OUT(1:N))
  DO I = 1, SIZE(ALLOC_ARRAY_OUT)
     ALLOC_ARRAY_OUT(I)%A = SIZE(ALLOC_ARRAY_OUT) - (I-1)
     ALLOC_ARRAY_OUT(I)%B = REAL(SIZE(ALLOC_ARRAY_OUT) - (I-1))
  END DO
  
  ! End of function.
END FUNCTION TEST_EXTENDED


! Create a test that pulls from a type defined in another file. This will
!  require that the Fortran wrapper USE's the other module, and that
!  that the Python wrapper has a definition of the type from the other file.
FUNCTION TEST_RETURN_AUX() RESULT(ANSWER)
  TYPE, BIND(C) :: T3
     INTEGER :: A
     REAL :: B
     CHARACTER :: C
  END TYPE T3
  TYPE(T3) :: ANSWER
  ANSWER%A = 1
  ANSWER%B = 2.0
  ANSWER%C = '3'
END FUNCTION TEST_RETURN_AUX
