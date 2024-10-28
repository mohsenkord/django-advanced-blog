{% extends "mail_templated/base.tpl" %}

{% block subject %}
<title>Email Verification</title>
{% endblock %}

{% block html %}
    <h1>Welcome to Our Service!</h1>
    <p>Thank you for registering. Please confirm your email by clicking the link below:</p>
    <p><a href="{{ confirmation_link }}">Confirm your email</a></p>
    <p>Your token is: <strong>{{ token }}</strong></p>
{% endblock %}
