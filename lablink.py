from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
import time
import pandas as pd
from bs4 import BeautifulSoup

# Safari WebDriver intialisieren
driver = webdriver.Safari()

try:
    # Schritt 1: Öffnen der Landingpage
    driver.get('[Enter Labindex URL]')
    WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "menu")))

    # Schritt 2: Klappen Sie den Bereich "Analysen" auf
    analyse_toggle = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//h3[contains(text(), 'Analysen')]"))
    )
    analyse_toggle.click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.doc-list a[title]")))

    # Schritt 3: Extrahieren der ersten 100 Links zu den Analysen
    analyse_links = driver.find_elements(By.CSS_SELECTOR, "div.doc-list a[title]")
    analyse_links = analyse_links[:100]  # Die ersten 100 Links
    print(f"Gefundene Links: {len(analyse_links)}")

    if len(analyse_links) == 0:
        print("Keine Links gefunden. Überprüfe den Selektor und die Seite.")

    # Initialisieren einer Liste zur Speicherung der extrahierten Daten
    all_data = []

    # Durchlaufen der ersten 1000 Links und Extraktion der Daten
    for i, link in enumerate(analyse_links):
        print(f"Klicke auf Link {i + 1}: {link.text}")

        # Warte, bis der Link anklickbar ist
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable(link))

        try:
            link.click()
            time.sleep(1)  # Pause von einer Sekunde nach jedem Klick, um das Laden zu ermöglichen
        except ElementNotInteractableException:
            print(f"Element nicht interagierbar für Link {i + 1}, erneuter Versuch...")
            time.sleep(2)
            link.click()

        # Wechseln zum "content"-Frame, wo der eigentliche Inhalt geladen wird
        driver.switch_to.default_content()
        WebDriverWait(driver, 10).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "content")))

        try:
            # Warte, bis der neue Inhalt vollständig geladen ist
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "div.document-title h2"))
            )

            # Extrahieren der Daten aus dem Container auf der neuen Seite
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            # Extrahiere den Titel des Analyts aus der "document-title"-Div
            title_container = soup.find('div', class_='document-title')
            title = title_container.find('h2').text.strip() if title_container and title_container.find(
                'h2') else "Kein Titel gefunden"
            data_dict = {"Link Nummer": i + 1, "Titel": title}  # Füge die Link-Nummer hinzu

            # Extrahiere die Tabelle aus der 'fr-view'-Div
            table_container = soup.find('div', class_='fr-view')
            if table_container:
                table_rows = table_container.find_all('tr')
                for row in table_rows:
                    cells = row.find_all('td')
                    if len(cells) == 2:
                        key = cells[0].text.strip()
                        value = cells[1].text.strip()
                        data_dict[key] = value

            # Hinzufügen der Daten zur Liste
            all_data.append(data_dict)

        except TimeoutException:
            print(f"Fehler beim Laden der Seite für Link {i + 1}. Speichern des Quellcodes zur Analyse.")
            driver.save_screenshot(f'error_link_{i + 1}.png')
            with open(f'page_source_link_{i + 1}.html', 'w', encoding='utf-8') as file:
                file.write(driver.page_source)

        # Zurück zum "menu"-Frame für den nächsten Link
        driver.switch_to.default_content()
        WebDriverWait(driver, 5).until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "menu")))

    # Umwandlung der Daten in ein DataFrame und Export in CSV
    if all_data:
        df = pd.DataFrame(all_data)
        df.to_csv('/Users/.../laboranalyte_daten.csv', index=False, encoding='utf-8')
        print("Daten erfolgreich in laboranalyte_daten.csv exportiert!")
    else:
        print("Keine Daten zum Exportieren vorhanden.")

except Exception as e:
    print(f"Ein Fehler ist aufgetreten: {e}")
    driver.save_screenshot('error_screenshot.png')  # Screenshot der Seite bei Fehler
    raise

finally:
    # Schließen des Browsers
    driver.quit()
