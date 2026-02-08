import time
import datetime
import pycozmo
from ps4Controle.ps4_controle import ps4_controle
from tkinter.filedialog import askdirectory
import os

# Variable pour stocker la dernière image reçue
latest_image = None
dir_img = None

def on_camera_image(cli, image):
    global latest_image
    latest_image = image

def controler_robots():
    global latest_image

    # Initialisation de la manette
    controller = ps4_controle()
    
    # Initialisation du robot
    cli = pycozmo.Client()
    cli.start()
    cli.connect()
    cli.wait_for_robot()
    
    # Activation de la caméra (en couleur)
    cli.enable_camera(enable=True, color=True)
    # Abonnement à l'événement de nouvelle image
    cli.add_handler(pycozmo.event.EvtNewRawCameraImage, on_camera_image)

    MAX_SPEED = 150.0  # mm/s
    MAX_HEAD_SPEED = 2.0 # rad/s
    MAX_LIFT_SPEED = 2.0 # rad/s

    print("Robot connecté. Utilisez la manette pour contrôler.")
    print("Joystick Gauche : Déplacement (Avancer/Reculer/Tourner)")
    print("Joystick Droit : Tête (Haut/Bas) et Bras (Gauche/Droite -> Haut/Bas)")
    print("Bouton TRIANGLE : Prendre une photo")
    print("Appuyez sur 'SHARE' pour quitter.")

    try:
        while True:
            controller.update()
            
            # Gestion des événements ponctuels (boutons appuyés)
            events = controller.getEvent()
            for event in events:
                if event == "TRIANGLE":
                    if latest_image:
                        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                        if dir_img is not None:
                            filename = os.path.join(dir_img, f"cozmo_photo_{timestamp}.png")
                        else:
                            filename = f"cozmo_photo_{timestamp}.png"
                        latest_image.save(filename)
                        print(f"Photo enregistrée : {filename}")
                    else:
                        print("Impossible de prendre la photo : aucune image caméra reçue pour l'instant.")
            
            # On vide la liste des événements traités
            controller.clearEvent()

            axes = controller.getAxes()
            buttons = controller.getButtons()

            # Quitter si SHARE est appuyé
            if buttons.get("SHARE", False):
                print("Arrêt du programme...")
                break
            
            # --- Déplacements ---
            speed_forward = -axes.get("LEFT_Y", 0.0) * MAX_SPEED
            speed_turn = axes.get("LEFT_X", 0.0) * MAX_SPEED
            
            l_wheel_speed = speed_forward + speed_turn
            r_wheel_speed = speed_forward - speed_turn
            
            l_wheel_speed = max(-MAX_SPEED, min(MAX_SPEED, l_wheel_speed))
            r_wheel_speed = max(-MAX_SPEED, min(MAX_SPEED, r_wheel_speed))

            if abs(l_wheel_speed) < 5 and abs(r_wheel_speed) < 5:
                cli.stop_all_motors()
            else:
                cli.drive_wheels(l_wheel_speed, r_wheel_speed)
            
            # --- Tête ---
            head_speed = -axes.get("RIGHT_Y", 0.0) * MAX_HEAD_SPEED
            if abs(head_speed) > 0.1:
                cli.move_head(head_speed)
            else:
                cli.move_head(0)
            
            # --- Bras (Lift) ---
            lift_speed = axes.get("RIGHT_X", 0.0) * MAX_LIFT_SPEED
            if abs(lift_speed) > 0.1:
                cli.move_lift(lift_speed)
            else:
                cli.move_lift(0)
                
            time.sleep(0.05)

    except KeyboardInterrupt:
        print("Interruption clavier.")
    finally:
        cli.stop_all_motors()
        cli.disconnect()
        cli.stop()
        print("Fin.")

def set_dir_img():
    out = None
    global dir_img
    while out == None:
        try :
            out = int(input("1.Selectionner le dossier\n2.Ecrire le dossier\n0.Annuler\n# "))
        except :
            print("Valeur invalide")
            out = None

    match out :
        case 1 :
            dir_img = askdirectory(
                initialdir=os.path.expanduser('~'),
                title="Sélectionnez votre dossier d'images"
            )
            print(f"Dossier selectionner {dir_img}")
        case 2 :
            dir_img = input("Dossier d'enregistrement des images : ")
            print(f"Dossier selectionner {dir_img}")
        case 0 :
            dir_img = None

def main():
    print("Programme de teste de la lib nexo-pycozmo avec manette de PS4")
    out = None
    while True:
        while out == None:
            try :
                out = int(input("1.Selectionner un dossier d'images\n2.Lancer\n# "))
            except :
                print("Valeur invalide")
                out = None
        match out:
            case 1 :
                set_dir_img()
                out = None
            case 2 :
                break
            case 0 :
                out = None


    controler_robots()

if __name__ == "__main__":
    main()
