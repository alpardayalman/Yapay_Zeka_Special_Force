APP_PATH1=Question-1
IMAGE_NAME1=sentiment-app

runlocal:
	sudo streamlit run $(APP_PATH1)/main.py

cleanlocal:
	sudo rm -f $(APP_PATH1)/sentiment_model.pkl $(APP_PATH1)/vectorizer.pkl


rundocker:
	sudo docker build -t $(IMAGE_NAME1) $(APP_PATH1)
	sudo docker run -p 8501:8501 $(IMAGE_NAME1)


cleandocker:
	sudo docker stop $(IMAGE_NAME1)-container || true
	sudo docker rm -v $(IMAGE_NAME1)-container || true
	sudo docker rmi -f $(IMAGE_NAME1) || true
	sudo docker system prune -f --volumes

clean: cleandocker cleanlocal
