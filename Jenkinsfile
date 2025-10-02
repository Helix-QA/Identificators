pipeline {

    agent { label "master" }
    
    parameters {
        choice(name: 'product', choices: ['Fitness', 'Stomatology','Salon'], description: 'Выберите продукт')
    }
    environment {
        releaseUser = "Админ"                                                       // Пользователь релизного хранилища
        workUser = "admin"                                                          // Пользователь рабочего хранилища
        dumpPathRelease = "D:\\Identificators\\Relis"                               // Путь выгрузки из релизного хранилища
        dumpPathWork = "D:\\Identificators\\Rab"                                    // Путь выгрузки из рабочего хранилища
        comparisonPath = "D:\\Identificators\\Obarabotka\\ПроверкаКонфигурации.epf" // Обработка сверки конфигурации
        verificationServer = "localhost/SverkaIdentif"                              // Пустая база для сверки конфигураций 
    }
    stages {
        stage('Подготовка .cf') {
            steps {
                script {
                    if (params.product == 'Fitness') {
                        
                        env.repRelease = "${env.repositoryReleaseFitness}"  
                        env.repWork = "${env.repositoryRabFitness}"         
                        env.releaseServer = "VAFitness"                   // Релизное хранилище
                        env.workServer = "Serv_Fitness_Rab"               // Рабочее хранилище 

                    } else if (params.product == 'Salon') {
                        
                        env.repRelease = "${env.repositoryReleaseSalon}"
                        env.repWork = "${env.repositoryRabSalon}"
                        env.releaseServer = "VASPA"                       // Релизное хранилище
                        env.workServer = "SPAsalonRab"                    // Рабочее хранилище 

                    } else {
                        
                        env.repRelease = "${env.repositoryReleaseStom}"
                        env.repWork = "${env.repositoryRabStom}"
                        env.releaseServer = "VAStoma"                         // Релизное хранилище
                        env.workServer = "Serv_Stoma_Rab"                     // Рабочее хранилище 
                    }
                }
            }
        }
      stage('Подключение и обновление из хранилища') {
            parallel {
                stage('Релизное') {
                    steps {
                        bat """
                        chcp 65001
                        @call vrunner session kill --db ${env.releaseServer} --db-user ${env.releaseUser} --uccode IDENTIF
                        @call vrunner loadrepo --storage-name ${env.repRelease} --storage-user ${env.VATest2} --ibconnection /Slocalhost/${env.releaseServer} --db-user ${env.releaseUser} --uccode IDENTIF
                        @call vrunner updatedb --ibconnection /Slocalhost/${env.releaseServer} --db-user ${env.releaseUser} --uccode IDENTIF
                        @call vrunner session unlock --db ${env.releaseServer} --db-user ${env.releaseUser}
                        """

                    }
                }
                stage('Рабочее') {
                    steps {
                        bat """
                        chcp 65001
                        @call vrunner session kill --db ${env.workServer} --db-user ${env.workUser} --uccode IDENTIF
                        @call vrunner loadrepo --storage-name ${env.repWork} --storage-user ${env.VATest2} --ibconnection /Slocalhost/${env.workServer} --db-user ${env.workUser} --uccode IDENTIF
                        @call vrunner updatedb --ibconnection /Slocalhost/${env.workServer} --db-user ${env.workUser} --uccode IDENTIF
                        @call vrunner session unlock --db ${env.workServer} --db-user ${env.workUser}
                        """
                    }
                }
            }
        }
        stage('Выгрузка XML') { 
            parallel {
                stage('Выгрузка из релизного') {
                    steps {
                        bat """
                        chcp 65001
                        @call vrunner decompile --out ${env.dumpPathRelease} --current --ibconnection /Slocalhost/${env.releaseServer} --db-user ${env.releaseUser}
                        """
                    }
                }
                stage('Выгрузка из рабочего') {
                    steps {
                        bat """
                        chcp 65001
                        @call vrunner decompile --out ${env.dumpPathWork} --current --ibconnection /Slocalhost/${env.workServer} --db-user ${env.workUser} 
                        """
                    }
                }
            }
        }
        stage('Сверка конфигурации') {
            steps {
                bat """
                chcp 65001
                "${env.platformPath}" /S"${verificationServer}" /Execute "${env.comparisonPath}"
                """
            }
        }
        stage('Отправка файла в чат') {
            steps {
                script {
                    def configuration_comparison_manager = 'IDENTIFICATOR/configuration_comparison_manager.py'
                    def telegram_file_sender = 'IDENTIFICATOR/telegram_file_sender.py'
                    bat "python ${configuration_comparison_manager}"
                    bat "python ${telegram_file_sender} ${params.product}"
                }
            }
        }
    }
    post{
        always{
                bat """
                chcp 65001
                @echo off
                echo Удаление всех файлов и папок в каталоге
                powershell -command "Get-ChildItem '${WORKSPACE}' -Recurse | Remove-Item -Recurse -Force"
                echo Удаление всех файлов и папок в каталоге
                powershell -command "Get-ChildItem '${dumpPathWork}' -Recurse | Remove-Item -Recurse -Force"
                echo Удаление всех файлов и папок в каталоге
                powershell -command "Get-ChildItem '${dumpPathRelease}' -Recurse | Remove-Item -Recurse -Force"
                echo Удаление завершено.
                """
        }
    }
}
