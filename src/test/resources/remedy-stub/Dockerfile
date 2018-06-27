FROM fedora:25

RUN dnf -y install procps net-tools pcre pcre-static python && \
    dnf clean all 
RUN pip install --upgrade pip
RUN pip install flask
RUN mkdir /remedy-stub

ENV FLASK_APP=/remedy-stub/app.py
ENV FLASK_ENV=development

COPY app /remedy-stub

VOLUME /remedy-stub

EXPOSE 5000

CMD flask run --host=0.0.0.0