APP_PATH1=Question-1
IMAGE_NAME1=sentiment-app

run1local:
	streamlit run $(APP_PATH1)/main.py

clean1local:
	rm -f $(APP_PATH1)/sentiment_model.pkl $(APP_PATH1)/vectorizer.pkl


run1docker:
	docker build -t $(IMAGE_NAME1) $(APP_PATH1)
	docker run -p 8501:8501 $(IMAGE_NAME1)


clean1docker:
	docker stop $(IMAGE_NAME1)-container || true
	docker rm -v $(IMAGE_NAME1)-container || true
	docker rmi -f $(IMAGE_NAME1) || true
	docker system prune -f --volumes

clean1: clean1docker clean1local