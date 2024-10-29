{% extends "mail_templated/base.tpl" %}

{% block subject %}
<title>Password recovery email</title>
{% endblock %}

{% block html %}
    <h1>Password Recovery</h1>
        <p>Hello,</p>
        <p>We received a request to reset your password. You can reset your password by clicking the link below:</p>
        <a href="{{ reset_link }}">Reset Password</a>
        <p>If you did not request a password reset, please ignore this email.</p>
        <p>Thank you!</p>
{% endblock %}