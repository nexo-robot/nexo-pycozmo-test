import pycozmo

def main():
    print("Programme de teste de la lib nexo-pycozmo")
    with pycozmo.connect() as cli:
        var = -1
        while var != 0:
            try :
                var = int(input("1.Avancer\n2.Reculer\n3.Tourner a gauche\n4.Tourner a droite\n0.Quitter\n# "))

                match var:
                    case 1 :
                        cli.drive_wheels(lwheel_speed=100, rwheel_speed=100)
                        print("Avancer")
                    case 2 :
                        cli.drive_wheels(lwheel_speed=-100, rwheel_speed=-100)
                        print("Reculer")
                    case 3 :
                        cli.drive_wheels(lwheel_speed=100, rwheel_speed=-100)
                        print("Droite")
                    case  4:
                        cli.drive_wheels(lwheel_speed=-100, rwheel_speed=100)
                        print("Gauche")
                    case 0:
                        var = -1

            except:
                print("Valeur invalide")


if __name__ == "__main__":
    main()
