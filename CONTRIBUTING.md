## Contribuciones

Para que no haya [gritos ni carreras](https://www.youtube.com/watch?v=6GEFwiXWieM) en el desarrollo de este repo ponemos 
unas pequeñas bases y líneas de desarrollo que sería buena idea seguir:

* :computer: :ok_hand: Comprobar que el código es capaz de ser interpretado sin errores antes de hacer push y antes de una PR
* :memo: :rainbow: Establecer **claramente** en el mensaje del commit lo que este está haciendo o solventando
* :zap: :heavy_exclamation_mark: Es preferible un solo commit que resuelva un issue que varios commits pequeños o 
que un commit añada código sin una función concreta
* :twisted_rightwards_arrows: :cop: La PR deberá ser comprobada y aprobada por los miembros del equipo a
los que se les haya asignado su revisión

En la creación de un nuevo issue se deberá especificar un objetivo claro y preferiblemente ir asignado a un [milestone](https://github.com/HBHackaton/api/milestones) y hacer un uso adecuado de las etiquetas si procede. Es recomendable incluir documentación adicional (guías u otros recursos) que ayuden a entender lo que el issue pretende resolver.


## Git workflow

- `master` Rama principal. A esta rama sólo se accede mediante PRs desde`dev` o `bugfix`. Esta la rama de producción versionada mediante tags y _releases_ de GitHub
- `dev` Rama de desarrollo. Desde esta rama se hacen las PRs a `master`. Esta rama se actualiza mediante PRs de ramas `feauture/<nombre_feature>`
- `feature` Rama de resolución de issues y otras bestias. En estas ramas se hará el principal desarrollo y se hará PR a `dev` cuando esté solventado el issue o nuevas funcionalidades. Se recomienda que los commits sean lo suficientemente aislados para completar un solo issue o funcionalidad. Se recomienda que el mensaje del commit resuelva el issue (ver Marcar issues como resueltos).
- `bugfix` Rama de solución rápida de bugs en master. Peligro. No tocar.

Algunas buenas prácticas y sugerencias:
- [Escribir un buen mensaje de commit](https://chris.beams.io/posts/git-commit/)
- [Marcar issues como resueltos desde el commit](https://help.github.com/articles/closing-issues-using-keywords/)
