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
use Symfony\Component\Console\Input\InputInterface;
use Symfony\Component\Console\Output\OutputInterface;

/**
 * @author Ivo Marino <ivo.marino@ttss.ch>
 */
class CheckinCommand extends Command
{

    protected function configure()
    {
        $this
            ->setName('checkin')
            ->setDescription('Push latest tenant configuration')
            ->setHelp(<<<EOT
<info>Encrypt and push the latest configuration for a given tenant to a repository</info>
EOT
            )
        ;
    }

    protected function execute(InputInterface $input, OutputInterface $output)
    {
         $output->writeln('TODO');
    }
}
