<?php

/*
 * This file is part of AppFlow.
 *
 * (c) Ivo Marino <ivo.marino@ttss.ch>
 *     Luca Di Maio <luca.dimaio@ttss.ch>
 *
 * For the full copyright and license information, please view the LICENSE
 * file that was distributed with this source code.
 */

namespace AppFlow\Command;

use Symfony\Component\Console\Command\Command;
use Symfony\Component\Console\Input\InputDefinition;
use Symfony\Component\Console\Input\InputOption;
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;
use Symfony\Component\Process\Process;
use Symfony\Component\Process\Exception\ProcessFailedException;

/**
 * @author Ivo Marino <ivo.marino@ttss.ch>
 */
class CheckoutCommand extends Command
{

    protected function configure()
    {
        $this
            ->setName('checkout')
            ->setDescription('Pull latest tenant configuration')
            ->setHelp(<<<EOT
<info>Pull the latest encrpyted configuration for a given tenant from a repository</info>
EOT
            )
            ->setDefinition(
                new InputDefinition(array(
                    new InputOption('tenant', 't', InputOption::VALUE_REQUIRED),
                    new InputOption('env', 'e', InputOption::VALUE_REQUIRED)
                ))
            );
        ;
    }

    protected function execute(InputInterface $input, OutputInterface $output)
    {
         # $output->writeln('TENANT: ' . $input->getOption('tenant') . ' ENV: ' . $input->getOption('env') );

         $process = new Process('ls -lsa');
         $process->run();

         // executes after the command finishes
         if (!$process->isSuccessful()) {
             throw new ProcessFailedException($process);
         }

         // echo $process->getOutput();
    }
}
